"""
ZELTA BQ Co-Pilot Service

Thin orchestration layer that calls the AI Brain through optimizer.answer_question.
This service:
- builds context pills
- normalizes brain/wallet context
- delegates the actual answer generation to the Brain
- formats the result into CopilotResponse
- provides a robust fallback if the Brain is unreachable
"""

import logging
from typing import Any, List, Optional
from datetime import datetime

from google.cloud import firestore
from optimizer import answer_question as brain_answer_question
from schemas.copilot import CopilotMessage, CopilotRequest, ContextPill, CopilotResponse, CopilotAPIResponse
# Set up logging
logger = logging.getLogger(__name__)

# --- UTILITIES ---

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
    return str(value).strip()


def _coerce_verdict_amount(value: Any) -> float:
    """Robust conversion of Naira strings or numbers to float."""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    
    text = str(value).strip()
    if not text:
        return 0.0
    
    # Remove currency symbols and formatting
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
        try:
            if isinstance(item, dict):
                label = _safe_str(item.get("label", ""))
                val = _safe_str(item.get("value", ""))
                if label or val:
                    pills.append(ContextPill(label=label, value=val))
            elif hasattr(item, "label") and hasattr(item, "value"):
                pills.append(
                    ContextPill(
                        label=_safe_str(getattr(item, "label", "")),
                        value=_safe_str(getattr(item, "value", "")),
                    )
                )
        except Exception:
            continue
    return pills


# --- CONTEXT NORMALIZATION ---

def _normalize_brain_context(brain_context: dict) -> dict:
    """
    Accepts nested or flat intelligence formats and returns the 
    standardized nested shape used by the Co-Pilot service.
    """
    brain_context = brain_context or {}

    # If already using the standard nested structure, return it
    if all(k in brain_context for k in ["stress", "bias", "allocation"]):
        return brain_context

    # Otherwise, map flat fields to nested objects
    return {
        "stress": {
            "combined_index": _safe_float(brain_context.get("stress_index"), 50.0),
            "level": _safe_str(brain_context.get("stress_level"), "MODERATE"),
            "label": _safe_str(brain_context.get("stress_label"), ""),
        },
        "bias": {
            "active_bias": _safe_str(brain_context.get("active_bias"), "Rational"),
            "confidence": _safe_str(brain_context.get("bias_confidence"), "Low"),
            "explanation": _safe_str(brain_context.get("bias_explanation"), ""),
        },
        "decision": {
            "verdict": _safe_str(brain_context.get("decision_verdict"), "HOLD"),
            "plain_english": _safe_str(brain_context.get("decision_plain"), ""),
            "edge": _safe_float(brain_context.get("edge"), 0.0),
            "win_probability": _safe_float(brain_context.get("win_probability"), 0.5),
        },
        "confidence": {
            "gap": _safe_float(brain_context.get("confidence_gap"), 0.0),
            "rational_pct": _safe_float(brain_context.get("rational_pct"), 50.0),
            "behavioral_pct": _safe_float(brain_context.get("behavioral_pct"), 50.0),
            "confidence_score": _safe_float(brain_context.get("confidence_score"), 50.0),
            "confidence_tier": _safe_str(brain_context.get("confidence_tier"), "Low"),
            "score_label": _safe_str(brain_context.get("score_label"), "WEAK"),
            "intervention_urgency": _safe_str(brain_context.get("intervention_urgency"), "LOW"),
            "plain_english": _safe_str(brain_context.get("confidence_plain"), ""),
        },
        "allocation": {
            "verdict": _safe_str(brain_context.get("verdict"), "HOLD"),
            "invest_ngn": _safe_float(brain_context.get("invest_ngn"), 0.0),
            "save_ngn": _safe_float(brain_context.get("save_ngn"), 0.0),
            "hold_ngn": _safe_float(brain_context.get("hold_ngn"), 0.0),
            "allocation_pct": _safe_float(brain_context.get("allocation_pct"), 0.0),
            "plain_english": _safe_str(brain_context.get("allocation_plain"), ""),
        },
        "score": {
            "score": _safe_float(brain_context.get("decision_score"), 1.0),
            "rating": _safe_str(brain_context.get("score_rating"), "Poor"),
        },
        "bayse": {
            "score": _safe_float(brain_context.get("bayse_score"), 50.0),
            "status": _safe_str(brain_context.get("bayse_status"), "MODERATE"),
            "market_title": _safe_str(brain_context.get("bayse_market"), "Unavailable"),
            "crowd_yes_price": _safe_float(brain_context.get("crowd_yes"), 0.5),
            "crowd_no_price": _safe_float(brain_context.get("crowd_no"), 0.5),
            "mid_price": _safe_float(brain_context.get("mid_price"), 0.5),
            "source": "ZELTA Intelligence",
        },
        "explanation": {
            "summary": _safe_str(brain_context.get("summary"), ""),
            "reasoning": _safe_str(brain_context.get("reasoning"), ""),
            "action": _safe_str(brain_context.get("action"), ""),
            "bias_explanation": _safe_str(brain_context.get("bias_explanation"), ""),
            "context_summary": _safe_str(brain_context.get("context_summary"), ""),
        },
        "nlp": {
            "aggregate_sentiment": _safe_float(brain_context.get("nlp_sentiment"), 0.0),
        },
    }


def _build_context_pills(brain_context: dict, wallet_context: dict) -> List[ContextPill]:
    """Builds visual markers for the chat based on current brain and wallet data."""
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


# --- MAIN SERVICE FUNCTIONS ---

async def answer_question(
    db: firestore.Client,
    uid: str,
    request: CopilotRequest,
    brain_context: dict,
    wallet_context: dict,
) -> CopilotResponse:
    """
    Orchestration: Normalizes inputs, calls the AI Brain via optimizer, 
    and validates the response.
    """
    _ = (db, uid)  # Placeholder for future message persistence logic

    # 1. Normalize local context and build initial UI markers
    normalized_brain = _normalize_brain_context(brain_context)
    local_pills = _build_context_pills(normalized_brain, wallet_context)

    # 2. Construct the full payload for the Brain
    history_list = [
    {"role": msg.role, "content": msg.content}
    for msg in (request.conversation_history or [])[-6:]
    ]

    brain_payload = {
    "question": request.question,   # ✅ REQUIRED
    "context": {
        "brain": normalized_brain,
        "wallet": wallet_context or {},
        "history": history_list,
        "context_pills": [pill.model_dump() for pill in local_pills],
        "user_id": uid,
      }
    }

    try:
        # 3. Call the Optimizer Client (hits /brain/v1/ask)
        result = await brain_answer_question(
                question=brain_payload["question"],
                context=brain_payload["context"],
            )

        success = bool(result.get("success", True))
        answer = _safe_str(
            result.get("answer"),
            "I could not generate a response just now. Please try again.",
        )

        if not success:
            logger.warning(f"Brain call unsuccessful for {uid}: {answer}")
            return _fallback_response(normalized_brain, local_pills)

        # 4. Clean and normalize fields from the Brain response
        verdict = _safe_str(result.get("verdict", "HOLD")).upper()
        if verdict not in {"SAVE", "INVEST", "HOLD"}:
            verdict = "HOLD"

        verdict_amount = _coerce_verdict_amount(result.get("verdict_amount"))
        confidence = _safe_float(result.get("confidence", 70.0), 70.0)
        sources = _safe_sources(result.get("sources"))
        
        # Use pills from Brain if provided, else keep local ones
        returned_pills = _safe_context_pills(result.get("context_pills", []))
        final_pills = returned_pills if returned_pills else local_pills

        return CopilotResponse(
            answer=answer,
            verdict=verdict,
            verdict_amount=0.0 if verdict == "HOLD" else verdict_amount,
            context_pills=final_pills,
            confidence=max(0.0, min(100.0, confidence)),
            sources=sources,
        )

    except Exception as e:
        logger.error(f"Co-Pilot orchestration failed for user {uid}: {str(e)}")
        return _fallback_response(normalized_brain, local_pills)


def _fallback_response(
    brain_context: dict,
    context_pills: List[ContextPill],
) -> CopilotResponse:
    """
    Emergency fallback using local Intelligence data when the LLM is down.
    """
    # brain_context is already normalized here by answer_question
    allocation = brain_context.get("allocation", {})
    explanation = brain_context.get("explanation", {})

    verdict = _safe_str(allocation.get("verdict", "HOLD"), "HOLD").upper()
    if verdict not in {"SAVE", "INVEST", "HOLD"}:
        verdict = "HOLD"

    amount = _safe_float(allocation.get("invest_ngn"), 0.0)
    plain = _safe_str(
        explanation.get("summary") or allocation.get("plain_english"),
        "Based on current market conditions, the BQ engine suggests holding."
    )

    return CopilotResponse(
        answer=f"{plain} (Note: AI Brain is temporarily offline — using BQ engine fallback.)",
        verdict=verdict,
        verdict_amount=0.0 if verdict == "HOLD" else amount,
        context_pills=context_pills,
        confidence=65.0,
        sources=["BQ Engine (fallback)", "Bayse Markets"],
    )
