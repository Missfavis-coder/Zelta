"""
ZELTA BQ Co-Pilot Service

Thin orchestration layer that calls the AI Brain through optimizer.answer_question.
This service only:
- builds context pills
- normalizes brain/wallet context
- delegates the actual answer generation to the Brain
- formats the result into CopilotResponse
"""

import logging
from typing import Any, Dict, List

from google.cloud import firestore

from optimizer import answer_question as brain_answer_question
from schemas.copilot import CopilotRequest, CopilotResponse, ContextPill

logger = logging.getLogger(__name__)


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _normalize_brain_context(brain_context: dict) -> dict:
    """
    Accept either:
      1) nested brain format:
         brain_context["stress"]["combined_index"]
      2) flat intelligence format:
         brain_context["stress_index"], brain_context["active_bias"], etc.

    Returns the nested shape used by the Co-Pilot service.
    """
    brain_context = brain_context or {}

    if "stress" in brain_context or "bias" in brain_context or "allocation" in brain_context:
        return brain_context

    return {
        "stress": {
            "combined_index": brain_context.get("stress_index", 50.0),
            "level": brain_context.get("stress_level", "MODERATE"),
            "label": brain_context.get("stress_label", ""),
        },
        "bias": {
            "active_bias": brain_context.get("active_bias", "Rational"),
            "confidence": brain_context.get("bias_confidence", "Low"),
            "explanation": brain_context.get("bias_explanation", ""),
        },
        "decision": {
            "verdict": brain_context.get("decision_verdict", "HOLD"),
            "plain_english": brain_context.get("decision_plain", ""),
            "edge": brain_context.get("edge", 0.0),
            "win_probability": brain_context.get("win_probability", 0.5),
        },
        "confidence": {
            "gap": brain_context.get("confidence_gap", 0.0),
            "rational_pct": brain_context.get("rational_pct", 50.0),
            "behavioral_pct": brain_context.get("behavioral_pct", 50.0),
            "confidence_score": brain_context.get("confidence_score", 50.0),
            "confidence_tier": brain_context.get("confidence_tier", "Low"),
            "score_label": brain_context.get("score_label", "WEAK"),
            "intervention_urgency": brain_context.get("intervention_urgency", "LOW"),
            "plain_english": brain_context.get("confidence_plain", ""),
        },
        "allocation": {
            "verdict": brain_context.get("verdict", "HOLD"),
            "invest_ngn": brain_context.get("invest_ngn", 0.0),
            "save_ngn": brain_context.get("save_ngn", 0.0),
            "hold_ngn": brain_context.get("hold_ngn", 0.0),
            "allocation_pct": brain_context.get("allocation_pct", 0.0),
            "plain_english": brain_context.get("allocation_plain", ""),
        },
        "score": {
            "score": brain_context.get("decision_score", 1.0),
            "decision_score": brain_context.get("decision_score", 1.0),
            "rating": brain_context.get("score_rating", "Poor"),
        },
        "bayse": {
            "score": brain_context.get("bayse_score", 50.0),
            "status": brain_context.get("bayse_status", "MODERATE"),
            "market_title": brain_context.get("bayse_market", "Unavailable"),
            "market_id": "",
            "crowd_yes_price": brain_context.get("crowd_yes", 0.5),
            "crowd_no_price": brain_context.get("crowd_no", 0.5),
            "mid_price": brain_context.get("mid_price", 0.5),
            "best_bid": 0.0,
            "best_ask": 0.0,
            "spread": brain_context.get("spread", 0.0),
            "imbalance": 0.0,
            "volume24h": 0.0,
            "trade_count_24h": 0,
            "available": True,
            "raw_crowd_stress": brain_context.get("stress_index", 50.0),
            "naira_weakness_probability": brain_context.get("crowd_yes", 0.5),
            "outcome": None,
            "last_price": 0.0,
            "source": "ZELTA Intelligence",
            "updated_at": None,
        },
        "explanation": {
            "summary": brain_context.get("summary", ""),
            "reasoning": "",
            "action": brain_context.get("action", ""),
            "what_this_means_for_you": None,
            "bias_explanation": brain_context.get("bias_explanation", ""),
            "confidence_note": brain_context.get("confidence_plain", ""),
            "bq_alert": brain_context.get("bq_alert", ""),
            "context_summary": brain_context.get("context_summary", ""),
        },
        "nlp": {
            "scored_headlines": [],
            "aggregate_sentiment": brain_context.get("nlp_sentiment", 0.0),
        },
    }


def _build_context_pills(brain_context: dict, wallet_context: dict) -> List[ContextPill]:
    brain_context = _normalize_brain_context(brain_context)

    stress_index = _safe_float(brain_context.get("stress", {}).get("combined_index", 50.0), 50.0)
    stress_level = _safe_str(brain_context.get("stress", {}).get("level", "MODERATE"), "MODERATE")
    active_bias = _safe_str(brain_context.get("bias", {}).get("active_bias", "Rational"), "Rational")
    free_cash = _safe_float(wallet_context.get("free_cash", 0.0), 0.0)
    verdict_amount = _safe_float(brain_context.get("allocation", {}).get("invest_ngn", 0.0), 0.0)

    return [
        ContextPill(label="Bayse Fear", value=f"{stress_index:.0f}%"),
        ContextPill(label="Bias", value=active_bias.replace("_", " ").title()),
        ContextPill(label="Free Cash", value=f"₦{free_cash:,.0f}"),
        ContextPill(label="Stress Level", value=stress_level),
        ContextPill(label="Kelly Amount", value=f"₦{verdict_amount:,.0f}"),
    ]


def _coerce_verdict_amount(value: Any) -> float:
    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if not text:
        return 0.0

    text = text.replace("₦", "").replace(",", "").strip()
    try:
        return float(text)
    except ValueError:
        return 0.0


def _safe_sources(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(v) for v in value if v is not None]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return ["Bayse Markets", "Wallet Data", "BQ Engine"]


def _safe_context_pills(value: Any) -> List[ContextPill]:
    pills: List[ContextPill] = []
    if not isinstance(value, list):
        return pills

    for item in value:
        if isinstance(item, dict):
            label = _safe_str(item.get("label", ""))
            pill_value = _safe_str(item.get("value", ""))
            if label or pill_value:
                pills.append(ContextPill(label=label, value=pill_value))
        elif hasattr(item, "label") and hasattr(item, "value"):
            pills.append(ContextPill(label=_safe_str(getattr(item, "label", "")), value=_safe_str(getattr(item, "value", ""))))
    return pills


async def answer_question(
    db: firestore.Client,
    uid: str,
    request: CopilotRequest,
    brain_context: dict,
    wallet_context: dict,
) -> CopilotResponse:
    """
    Send user question to the Brain via optimizer.answer_question()
    and return a structured CopilotResponse.
    """
    _ = (db, uid)  # reserved for future chat history persistence

    brain_context = _normalize_brain_context(brain_context)
    context_pills = _build_context_pills(brain_context, wallet_context)

    brain_payload = {
        "brain": brain_context,
        "wallet": wallet_context or {},
        "history": [
            {"role": msg.role, "content": msg.content}
            for msg in (request.conversation_history or [])[-6:]
        ],
        "context_pills": [{"label": pill.label, "value": pill.value} for pill in context_pills],
        "user_id": uid,
    }

    try:
        result = await brain_answer_question(
            question=request.question,
            context=brain_payload,
        )

        success = bool(result.get("success", True))
        answer = _safe_str(
            result.get("answer"),
            "I could not generate a response just now. Please try again.",
        )

        verdict = _safe_str(result.get("verdict", "HOLD")).upper()
        if verdict not in {"SAVE", "INVEST", "HOLD"}:
            verdict = "HOLD"

        verdict_amount = _coerce_verdict_amount(result.get("verdict_amount"))
        confidence = _safe_float(result.get("confidence", 70.0), 70.0)
        sources = _safe_sources(result.get("sources"))
        returned_pills = _safe_context_pills(result.get("context_pills", [])) or context_pills

        if not success:
            raise RuntimeError(_safe_str(result.get("answer"), "Brain returned an unsuccessful response."))

        return CopilotResponse(
            answer=answer,
            verdict=verdict,
            verdict_amount=0.0 if verdict == "HOLD" else verdict_amount,
            context_pills=returned_pills,
            confidence=max(0.0, min(100.0, confidence)),
            sources=sources,
        )

    except Exception as e:
        logger.error("Copilot Brain call failed: %s", e)
        return _fallback_response(brain_context, context_pills)


def _fallback_response(
    brain_context: dict,
    context_pills: list,
) -> CopilotResponse:
    """
    Local fallback if the Brain copilot route is unavailable.
    """
    brain_context = _normalize_brain_context(brain_context)
    allocation = brain_context.get("allocation", {})

    verdict = _safe_str(allocation.get("verdict", "HOLD"), "HOLD").upper()
    if verdict not in {"SAVE", "INVEST", "HOLD"}:
        verdict = "HOLD"

    amount = _safe_float(allocation.get("invest_ngn", allocation.get("invest_amount", 0.0)), 0.0)
    plain = _safe_str(
        allocation.get("plain_english"),
        "The BQ engine recommends HOLD at current stress levels.",
    )

    return CopilotResponse(
        answer=f"{plain} (Note: AI Brain temporarily unavailable — using local BQ fallback.)",
        verdict=verdict,
        verdict_amount=0.0 if verdict == "HOLD" else amount,
        context_pills=context_pills,
        confidence=65.0,
        sources=["BQ Engine (fallback)", "Bayse Markets"],
    )
