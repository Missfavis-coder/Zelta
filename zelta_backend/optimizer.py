"""
ZELTA Optimizer — AI Brain HTTP Client

Single point of contact between ZELTA backend and the deployed Brain.
It:
  - Calls POST /brain/intelligence
  - Sends wallet_data, transactions, user_context
  - Returns a normalized brain dict
  - Provides Bayse and stress helper fetchers
  - Provides a direct Copilot question-answering helper
"""

import json
import logging
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

import httpx

from config.settings import settings

logger = logging.getLogger(__name__)

BRAIN_TIMEOUT = 30.0
COPILOT_TIMEOUT = 20.0


def _base_url() -> str:
    return settings.ai_brain_url.rstrip("/")


def _brain_url(path: str) -> str:
    return f"{_base_url()}/{path.lstrip('/')}"


def _brain_headers() -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if getattr(settings, "internal_api_key", ""):
        headers["x-api-key"] = settings.internal_api_key
    return headers


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def _safe_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _safe_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> list:
    return value if isinstance(value, list) else []


def _json_safe(value: Any) -> Any:
    """
    Recursively convert non-JSON-serializable values into JSON-safe values.
    Important for Firestore timestamps and similar objects.
    """
    if value is None:
        return None

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    iso = getattr(value, "isoformat", None)
    if callable(iso):
        try:
            return iso()
        except Exception:
            pass

    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}

    if isinstance(value, list):
        return [_json_safe(v) for v in value]

    if isinstance(value, tuple):
        return [_json_safe(v) for v in value]

    return value


def _extract_body(data: Any) -> dict:
    """
    Handles:
      1) {"success": true, "data": {...}}
      2) {"data": {...}}
      3) {...}
    """
    if isinstance(data, dict):
        inner = data.get("data")
        if isinstance(inner, dict):
            return inner
        return data
    return {}


def _brain_payload(
    wallet_data: Optional[dict],
    transactions: Optional[List[dict]],
    user_context: Optional[dict],
) -> dict:
    wallet_data = wallet_data or {}
    transactions = transactions or []
    user_context = user_context or {}

    payload = {
        "wallet_data": {
            "free_cash": _safe_float(wallet_data.get("free_cash", 0.0)),
            "locked_total": _safe_float(
                wallet_data.get("locked_total", wallet_data.get("locked_amount", 0.0))
            ),
            "total_balance": _safe_float(wallet_data.get("total_balance", 0.0)),
        },
        "transactions": transactions,
        "user_context": user_context,
    }

    return _json_safe(payload)


def _copilot_payload(question: str, context: Optional[dict]) -> dict:
    return _json_safe(
        {
            "question": question,
            "context": context or {},
        }
    )


async def _post_json(path: str, payload: dict, timeout: float) -> dict:
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            _brain_url(path),
            headers=_brain_headers(),
            json=payload,
        )

    logger.info("Brain route=%s status=%s body=%s", path, resp.status_code, resp.text)
    if resp.status_code in (401, 403, 404, 422):
        raise RuntimeError(f"{path} rejected request: {resp.status_code} {resp.text}")

    resp.raise_for_status()
    return resp.json()


async def _get_json(path: str, timeout: float) -> dict:
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.get(
            _brain_url(path),
            headers=_brain_headers(),
        )

    logger.info("Brain GET route=%s status=%s body=%s", path, resp.status_code, resp.text)
    if resp.status_code in (401, 403, 404, 422):
        raise RuntimeError(f"{path} rejected request: {resp.status_code} {resp.text}")

    resp.raise_for_status()
    return resp.json()


async def run_brain(
    wallet_data: Optional[dict] = None,
    profile_data: Optional[dict] = None,
    transaction_patterns: Optional[dict] = None,
    mode: str = "full",  # "fast" | "full" | "legacy"
) -> dict:
    """
    Call the deployed ZELTA AI Brain and return a normalized dict.

    Route priority:
      1) /brain/v1/intelligence
      
      3) legacy fallback routes if needed
    """
    wallet_data = wallet_data or {}
    profile_data = profile_data or {}
    transaction_patterns = transaction_patterns or {}

    free_cash = _safe_float(wallet_data.get("free_cash", 0.0))

    transactions: List[dict] = []
    user_context: dict = _safe_dict(profile_data)

    if isinstance(transaction_patterns, dict):
        if "transactions" in transaction_patterns:
            transactions = _safe_list(transaction_patterns.get("transactions"))
            extras = {k: v for k, v in transaction_patterns.items() if k != "transactions"}
            if extras:
                user_context = {**user_context, **extras}
        else:
            user_context = {**user_context, **transaction_patterns}
    elif isinstance(transaction_patterns, list):
        transactions = transaction_patterns

    payload = _brain_payload(wallet_data, transactions, user_context)

    route_candidates = [
        f"/brain/v1/intelligence",
        "/brain/pipeline/full",
        "/brain/pipeline/fast",
    ]

    last_error = ""
    for route in route_candidates:
        try:
            data = await _post_json(route, payload, timeout=BRAIN_TIMEOUT)

            if isinstance(data, str):
                logger.error("Brain returned a string response: %s", data)
                return normalise_brain_response(_fallback_brain_response(free_cash))

            if isinstance(data, dict) and data.get("success") is False:
                logger.error("Brain returned success=false: %s", data)
                return normalise_brain_response(_fallback_brain_response(free_cash))

            body = _extract_body(data)
            return normalise_brain_response(body)

        except Exception as e:
            last_error = str(e)
            logger.warning("Brain route failed (%s): %s", route, e)

    logger.error("Brain call failed after all routes: %s", last_error)
    return normalise_brain_response(_fallback_brain_response(free_cash))


async def answer_question(
    question: str,
    context: Optional[dict] = None,
) -> dict:
    """
    Call the Brain Copilot route and return a normalized answer payload.
    Priority updated to include the confirmed /brain/v1/ask endpoint.
    """
    payload = _copilot_payload(question, context)

    # Added the confirmed v1 route as the first candidate
    route_candidates = [
        "/brain/v1/ask",
        "/brain/ask",
        "/api/ask",
        "/brain/copilot",
        "/api/copilot",
    ]

    last_error = ""
    for route in route_candidates:
        try:
            # _post_json handles headers (x-api-key) and standard error raises
            data = await _post_json(route, payload, timeout=COPILOT_TIMEOUT)

            if isinstance(data, dict):
                body = _extract_body(data)

                # Extract answer from the "data" or "response" field
                answer = _safe_str(body.get("answer") or body.get("response"), "")
                if not answer:
                    answer = "I could not generate a response just now. Please try again."

                # Normalizing Verdict (INVEST, SAVE, or HOLD)
                verdict = _safe_str(body.get("verdict", "HOLD"), "HOLD").upper()
                if verdict not in {"SAVE", "INVEST", "HOLD"}:
                    verdict = "HOLD"

                # Cleaning and converting Naira strings or raw numbers to float
                verdict_amount = body.get("verdict_amount", body.get("amount", 0.0))
                if isinstance(verdict_amount, str):
                    cleaned = verdict_amount.replace("₦", "").replace(",", "").strip()
                    try:
                        verdict_amount = float(cleaned)
                    except ValueError:
                        verdict_amount = 0.0
                else:
                    verdict_amount = _safe_float(verdict_amount, 0.0)

                confidence = _safe_float(body.get("confidence", 70.0), 70.0)

                sources = body.get("sources", ["Bayse Markets", "Wallet Data", "BQ Engine"])
                if not isinstance(sources, list):
                    sources = [str(sources)]

                context_pills = body.get("context_pills", [])
                if not isinstance(context_pills, list):
                    context_pills = []

                return {
                    "success": True,
                    "answer": answer,
                    "verdict": verdict,
                    "verdict_amount": 0.0 if verdict == "HOLD" else verdict_amount,
                    "confidence": max(0.0, min(100.0, confidence)),
                    "sources": sources,
                    "context_pills": context_pills,
                    "raw": body,
                }

            last_error = f"Unexpected response type from {route}"

        except Exception as e:
            last_error = str(e)
            # If we hit a 404, we continue to the next candidate
            if "404" in last_error:
                logger.warning("Route %s not found (404). Trying next...", route)
                continue
            logger.warning("Copilot route failed (%s): %s", route, e)

    # Final fallback if all candidates fail
    logger.error("Copilot call failed after all routes: %s", last_error)
    return {
        "success": False,
        "answer": "The AI Brain Copilot is temporarily unavailable.",
        "verdict": "HOLD",
        "verdict_amount": 0.0,
        "confidence": 65.0,
        "sources": ["BQ Engine (local)", "Bayse Markets"],
        "context_pills": [],
        "raw": {"error": last_error},
    }


async def _get_signal_json(paths: Sequence[str], timeout: float = 15.0) -> Tuple[dict, str]:
    """
    Try multiple endpoints and return the first usable JSON payload.
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        last_error = ""
        for path in paths:
            try:
                data = await _get_json(path, timeout=timeout)
                if isinstance(data, dict):
                    return data, path
                last_error = f"Non-dict response from {path}"
            except Exception as exc:
                last_error = str(exc)

    raise RuntimeError(last_error or "No signal endpoint available")


async def fetch_bayse_signal() -> dict:
    """
    Fetch Bayse signal from the Brain service.
    """
    try:
        data, _ = await _get_signal_json(("/api/stress", "/stress", "/bayse"))
        raw = data.get("data", data)
        raw = raw.get("bayse", raw) if isinstance(raw, dict) else raw
        return _normalise_bayse(raw if isinstance(raw, dict) else {})
    except Exception as e:
        logger.warning("Bayse-only fetch failed: %s", e)
        return _fallback_bayse()


async def fetch_stress_signal() -> dict:
    """
    Fetch stress index from the Brain service.
    """
    try:
        data, _ = await _get_signal_json(("/api/stress", "/stress"))
        raw = data.get("data", data)
        raw = raw.get("stress", raw) if isinstance(raw, dict) else raw
        return _normalise_stress(raw if isinstance(raw, dict) else {})
    except Exception as e:
        logger.warning("Stress-only fetch failed: %s", e)
        return _fallback_stress()


def _normalise_bayse(raw: dict) -> dict:
    raw = raw or {}
    score = _safe_float(raw.get("score", 50.0))
    mid_price = _safe_float(raw.get("mid_price", 0.5))
    yes_prob = _safe_float(
        raw.get("naira_weakness_probability", round(mid_price * 100, 2)),
        round(mid_price * 100, 2),
    )

    return {
        "score": score,
        "status": _safe_str(raw.get("status", "MODERATE"), "MODERATE"),
        "market_title": _safe_str(raw.get("market_title", ""), ""),
        "market_id": _safe_str(raw.get("market_id", ""), ""),
        "crowd_yes_price": _safe_float(raw.get("crowd_yes_price", 0.5)),
        "crowd_no_price": _safe_float(raw.get("crowd_no_price", 0.5)),
        "mid_price": mid_price,
        "best_bid": _safe_float(raw.get("best_bid", 0.0)),
        "best_ask": _safe_float(raw.get("best_ask", 0.0)),
        "spread": _safe_float(raw.get("spread", 0.0)),
        "imbalance": _safe_float(raw.get("imbalance", 0.0)),
        "volume24h": _safe_float(raw.get("volume24h", 0.0)),
        "trade_count_24h": _safe_int(raw.get("trade_count_24h", 0)),
        "available": _safe_bool(raw.get("available", True)),
        "raw_crowd_stress": _safe_float(raw.get("raw_crowd_stress", score)),
        "naira_weakness_probability": yes_prob,
        "cbn_rate_fear_index": score,
        "inflation_anxiety_score": score,
        "usd_ngn_threshold_probability": yes_prob,
    }


def _normalise_stress(raw: dict) -> dict:
    raw = raw or {}
    score = _safe_float(raw.get("score", raw.get("stress_score", 50.0)))
    components = _safe_dict(raw.get("components"))

    return {
        "combined_index": score,
        "level": _safe_str(raw.get("level", "MODERATE"), "MODERATE"),
        "label": _safe_str(raw.get("plain_english", raw.get("label", "")), ""),
        "bayse_primary": _safe_float(components.get("bayse_stress", 0.0)),
        "nlp_secondary": _safe_float(components.get("nlp_stress", 0.0)),
        "bayse_weight": _safe_float(components.get("bayse_weight", 0.6), 0.6),
        "nlp_weight": _safe_float(components.get("nlp_weight", 0.4), 0.4),
        "market_probability": _safe_float(components.get("market_probability", 0.5), 0.5),
    }


def _normalise_bias(raw: dict) -> dict:
    raw = raw or {}
    return {
        "active_bias": _safe_str(raw.get("active_bias", raw.get("bias", "Rational")), "Rational"),
        "confidence": _safe_str(raw.get("confidence", "Low"), "Low"),
        "explanation": _safe_str(raw.get("explanation", ""), ""),
        "inputs": _safe_dict(raw.get("inputs")),
    }


def _normalise_decision(raw: dict) -> dict:
    raw = raw or {}
    return {
        "verdict": _safe_str(raw.get("verdict", "HOLD"), "HOLD"),
        "market_probability": _safe_float(raw.get("market_probability", 0.5)),
        "rational_probability": _safe_float(raw.get("rational_probability", 0.5)),
        "edge": _safe_float(raw.get("edge", 0.0)),
        "confidence": _safe_str(raw.get("confidence", "Low"), "Low"),
        "win_probability": _safe_float(raw.get("win_probability", 0.5)),
        "bias_applied": _safe_str(raw.get("bias_applied", "Rational"), "Rational"),
        "plain_english": _safe_str(raw.get("plain_english", ""), ""),
    }


def _normalise_confidence(raw: dict) -> dict:
    raw = raw or {}
    return {
        "rational_pct": _safe_float(raw.get("rational_pct", 50.0)),
        "behavioral_pct": _safe_float(raw.get("behavioral_pct", 50.0)),
        "gap": _safe_float(raw.get("gap", 0.0)),
        "confidence_score": _safe_float(raw.get("confidence_score_100", raw.get("confidence_score", 50.0))),
        "confidence_tier": _safe_str(raw.get("confidence_tier", raw.get("confidence_label", "Low")), "Low"),
        "score_label": _safe_str(raw.get("score_label", "WEAK"), "WEAK"),
        "intervention_urgency": _safe_str(raw.get("intervention_urgency", "MODERATE"), "MODERATE"),
        "is_actionable": _safe_bool(raw.get("is_actionable", False)),
        "plain_english": _safe_str(raw.get("plain_english", ""), ""),
        "metrics": _safe_dict(raw.get("metrics")),
    }


def _normalise_allocation(raw: dict) -> dict:
    raw = raw or {}
    return {
        "verdict": _safe_str(raw.get("verdict", "HOLD"), "HOLD"),
        "invest_amount": _safe_float(raw.get("invest_ngn", raw.get("invest_amount", 0.0))),
        "save_amount": _safe_float(raw.get("save_ngn", raw.get("save_amount", 0.0))),
        "hold_amount": _safe_float(raw.get("hold_ngn", raw.get("hold_amount", 0.0))),
        "allocation_pct": _safe_float(raw.get("allocation_pct", 0.0)),
        "allocator_notes": _safe_str(raw.get("allocator_notes", ""), ""),
        "plain_english": _safe_str(raw.get("plain_english", ""), ""),
    }


def _normalise_score(raw: dict) -> dict:
    raw = raw or {}
    return {
        "score": _safe_float(raw.get("score", raw.get("decision_score", 1.0)), 1.0),
        "decision_score": _safe_float(raw.get("decision_score", raw.get("score", 1.0)), 1.0),
        "rating": _safe_str(raw.get("rating", "Poor"), "Poor"),
        "components": _safe_dict(raw.get("components")),
    }


def normalise_brain_response(raw_data: dict) -> dict:
    """
    Normalise the full brain response dict into ZELTA's internal structure.
    All backend services consume this shape.
    """
    raw_data = raw_data or {}

    # Flat intelligence report -> nested shape
    if any(
        k in raw_data
        for k in (
            "stress_index",
            "stress_level",
            "bayse_score",
            "bayse_market",
            "decision_verdict",
            "confidence_score",
            "allocation_plain",
            "score_rating",
        )
    ) and not any(
        k in raw_data
        for k in ("bayse", "nlp", "stress", "bias", "decision", "confidence", "allocation", "score", "explanation")
    ):
        stress_index = _safe_float(raw_data.get("stress_index", 50.0))
        bayse_score = _safe_float(raw_data.get("bayse_score", 50.0))
        market_probability = _safe_float(raw_data.get("market_probability", 0.5))

        return {
            "bayse": _normalise_bayse(
                {
                    "score": bayse_score,
                    "status": raw_data.get("bayse_status", "MODERATE"),
                    "market_title": raw_data.get("bayse_market", "Unavailable"),
                    "crowd_yes_price": raw_data.get("crowd_yes", 0.5),
                    "crowd_no_price": raw_data.get("crowd_no", 0.5),
                    "mid_price": raw_data.get("mid_price", 0.5),
                    "spread": raw_data.get("spread", 0.0),
                    "available": True,
                }
            ),
            "nlp": {
                "scored_headlines": raw_data.get("headlines", []),
                "aggregate_sentiment": _safe_float(raw_data.get("nlp_sentiment", 0.0)),
            },
            "stress": _normalise_stress(
                {
                    "score": stress_index,
                    "level": raw_data.get("stress_level", "MODERATE"),
                    "plain_english": raw_data.get("stress_label", ""),
                    "components": {
                        "bayse_stress": raw_data.get("bayse_primary", stress_index),
                        "nlp_stress": raw_data.get("nlp_secondary", 50.0),
                        "market_probability": market_probability,
                    },
                }
            ),
            "bias": _normalise_bias(
                {
                    "active_bias": raw_data.get("active_bias", "Rational"),
                    "confidence": raw_data.get("bias_confidence", "Low"),
                    "explanation": raw_data.get("bias_explanation", ""),
                    "inputs": {
                        "stress_score": stress_index,
                        "sentiment": _safe_float(raw_data.get("nlp_sentiment", 0.0)),
                        "market_probability": market_probability,
                    },
                }
            ),
            "decision": _normalise_decision(
                {
                    "verdict": raw_data.get("decision_verdict", "HOLD"),
                    "market_probability": market_probability,
                    "rational_probability": market_probability,
                    "edge": raw_data.get("edge", 0.0),
                    "confidence": raw_data.get("confidence_tier", "Low"),
                    "win_probability": raw_data.get("win_probability", 0.5),
                    "bias_applied": raw_data.get("active_bias", "Rational"),
                    "plain_english": raw_data.get("decision_plain", ""),
                }
            ),
            "confidence": _normalise_confidence(
                {
                    "rational_pct": raw_data.get("rational_pct", 50.0),
                    "behavioral_pct": raw_data.get("behavioral_pct", 50.0),
                    "gap": raw_data.get("confidence_gap", 0.0),
                    "confidence_score": raw_data.get("confidence_score", 50.0),
                    "confidence_tier": raw_data.get("confidence_tier", "Low"),
                    "score_label": raw_data.get("score_label", "WEAK"),
                    "intervention_urgency": raw_data.get("intervention_urgency", "LOW"),
                    "is_actionable": raw_data.get("is_actionable", False),
                    "plain_english": raw_data.get("confidence_plain", ""),
                    "metrics": raw_data.get("metrics", {}),
                }
            ),
            "allocation": _normalise_allocation(
                {
                    "verdict": raw_data.get("verdict", "HOLD"),
                    "invest_amount": raw_data.get("invest_ngn", 0.0),
                    "save_amount": raw_data.get("save_ngn", 0.0),
                    "hold_amount": raw_data.get("hold_ngn", 0.0),
                    "allocation_pct": raw_data.get("allocation_pct", 0.0),
                    "allocator_notes": raw_data.get("allocator_notes", ""),
                    "plain_english": raw_data.get("allocation_plain", ""),
                }
            ),
            "score": _normalise_score(
                {
                    "score": raw_data.get("decision_score", 1.0),
                    "decision_score": raw_data.get("decision_score", 1.0),
                    "rating": raw_data.get("score_rating", "Poor"),
                    "components": raw_data.get("components", {}),
                }
            ),
            "explanation": {
                "summary": raw_data.get("summary", ""),
                "reasoning": raw_data.get("reasoning", ""),
                "action": raw_data.get("action", ""),
                "what_this_means_for_you": raw_data.get("what_this_means_for_you", ""),
                "bias_explanation": raw_data.get("bias_explanation", ""),
                "confidence_note": raw_data.get("confidence_plain", ""),
                "bq_alert": raw_data.get("bq_alert", ""),
                "context_summary": raw_data.get("context_summary", ""),
            },
        }

    return {
        "bayse": _normalise_bayse(raw_data.get("bayse", {})),
        "nlp": raw_data.get("nlp", {}),
        "stress": _normalise_stress(raw_data.get("stress", {})),
        "bias": _normalise_bias(raw_data.get("bias", {})),
        "decision": _normalise_decision(raw_data.get("decision", {})),
        "confidence": _normalise_confidence(raw_data.get("confidence", {})),
        "allocation": _normalise_allocation(raw_data.get("allocation", {})),
        "score": _normalise_score(raw_data.get("score", {})),
        "explanation": _safe_dict(raw_data.get("explanation", {})),
    }


def _fallback_bayse() -> dict:
    return {
        "score": 50.0,
        "status": "MODERATE",
        "market_title": "Unavailable",
        "market_id": "",
        "crowd_yes_price": 0.5,
        "crowd_no_price": 0.5,
        "mid_price": 0.5,
        "best_bid": 0.0,
        "best_ask": 0.0,
        "spread": 0.0,
        "imbalance": 0.0,
        "volume24h": 0.0,
        "trade_count_24h": 0,
        "raw_crowd_stress": 50.0,
        "naira_weakness_probability": 50.0,
        "cbn_rate_fear_index": 50.0,
        "inflation_anxiety_score": 50.0,
        "usd_ngn_threshold_probability": 50.0,
        "available": False,
    }


def _fallback_stress() -> dict:
    return {
        "combined_index": 50.0,
        "level": "MODERATE",
        "label": "Unable to reach AI Brain. Using neutral defaults.",
        "bayse_primary": 50.0,
        "nlp_secondary": 50.0,
        "bayse_weight": 0.6,
        "nlp_weight": 0.4,
        "market_probability": 0.5,
    }


def _fallback_brain_response(free_cash: float = 0.0) -> dict:
    return {
        "bayse": {
            "score": 50.0,
            "status": "MODERATE",
            "crowd_yes_price": 0.5,
            "crowd_no_price": 0.5,
            "mid_price": 0.5,
            "spread": 0.0,
            "imbalance": 0.0,
            "volume24h": 0.0,
            "trade_count_24h": 0,
            "market_title": "Unavailable",
            "market_id": "",
        },
        "nlp": {"scored_headlines": [], "aggregate_sentiment": 0.0},
        "stress": {
            "score": 50,
            "stress_score": 50,
            "level": "MODERATE",
            "plain_english": "AI Brain temporarily unavailable. Using safe neutral defaults.",
            "components": {
                "bayse_stress": 0.5,
                "nlp_stress": 0.5,
                "market_probability": 0.5,
                "bayse_weight": 0.6,
                "nlp_weight": 0.4,
            },
            "raw": {},
        },
        "bias": {
            "bias": "Rational",
            "active_bias": "Rational",
            "confidence": "Low",
            "explanation": "AI Brain unavailable. Defaulting to rational baseline.",
            "inputs": {},
        },
        "decision": {
            "market_probability": 0.5,
            "rational_probability": 0.5,
            "edge": 0.0,
            "confidence": "Low",
            "verdict": "HOLD",
            "plain_english": "AI Brain unavailable. HOLD all positions.",
            "win_probability": 0.5,
            "bias_applied": "Rational",
            "stress_score": 50,
        },
        "confidence": {
            "rational_pct": 50,
            "behavioral_pct": 50,
            "gap": 0,
            "confidence_score_100": 50,
            "confidence_score": 50,
            "confidence_tier": "Low",
            "score_label": "WEAK",
            "intervention_urgency": "LOW",
            "is_actionable": False,
            "plain_english": "Signal unavailable. No action recommended.",
            "metrics": {},
        },
        "allocation": {
            "verdict": "HOLD",
            "invest_ngn": 0.0,
            "save_ngn": 0.0,
            "hold_ngn": free_cash,
            "allocation_pct": 0.0,
            "allocator_notes": "AI Brain unavailable. Capital protected.",
            "plain_english": f"Hold ₦{free_cash:,.0f}. AI Brain temporarily offline.",
        },
        "score": {
            "score": 1.0,
            "decision_score": 1.0,
            "rating": "Poor",
            "components": {
                "edge_score": 0.0,
                "confidence_score": 0.0,
                "verdict_score": 0.5,
            },
        },
        "explanation": {
            "summary": "AI Brain unavailable.",
            "reasoning": "Could not reach the centralised AI Brain. All positions held.",
            "action": "Hold current positions.",
            "confidence_note": "No signal available.",
            "bq_alert": "AI Brain offline. Using safe fallback.",
            "context_summary": "",
        },
    }
