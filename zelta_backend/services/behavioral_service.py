"""
ZELTA Behavioral Service

Behavioral Snapshot:
Explains why ZELTA flagged the user's current behavior as irrational.

It combines:
1. Latest AI Brain output
2. Recent wallet transactions from Firestore
3. Simple correction logic for instinct vs math

This service does NOT run the full pipeline in the frontend.
It only prepares a human-readable behavioral explanation.
"""

import logging
from typing import Any, Dict, List, Optional

from datetime import datetime, timezone
from google.cloud import firestore

from optimizer import run_brain
from services.wallet_service import get_wallet_summary
from schemas.behavioral import (
    BehavioralEvidence,
    BehavioralSnapshot,
    BayseContext,
    InstinctSay,
    MathSay,
)

logger = logging.getLogger(__name__)


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _format_amount(amount: float) -> str:
    return f"₦{amount:,.0f}"


def _get_transactions_ref(db: firestore.Client, uid: str):
    return (
        db.collection("users")
        .document(uid)
        .collection("transactions")
        .order_by("date", direction=firestore.Query.DESCENDING)
        .limit(10)
    )


async def _load_recent_transactions(db: firestore.Client, uid: str) -> List[Dict[str, Any]]:
    """
    Load recent transactions from Firestore.
    """
    try:
        docs = _get_transactions_ref(db, uid).stream()
        return [doc.to_dict() for doc in docs if doc.to_dict()]
    except Exception as exc:
        logger.exception("Failed to load recent transactions: %s", exc)
        return []


def _detect_trigger(txn: Dict[str, Any], bias_name: str) -> str:
    """
    Simple explanation for what likely triggered the bias.
    """
    txn_type = str(txn.get("type", "")).lower()
    category = str(txn.get("category", "unknown")).lower()
    description = str(txn.get("description", "")).lower()
    amount = _safe_float(txn.get("amount", 0.0))

    if txn_type == "expense" and amount >= 5000:
        return f"Large spend in {category}"
    if "cash" in category or "withdraw" in description:
        return "Cash withdrawal"
    if "asuu" in description or "strike" in description:
        return "Stress reaction to campus news"
    if "panic" in description or "fear" in description:
        return "Panic-driven action"
    if bias_name.lower() == "loss aversion":
        return "Fear of losing money"
    if bias_name.lower() == "present bias":
        return "Short-term spending pressure"
    if bias_name.lower() == "mental accounting":
        return "Treating money as separate buckets"
    return "Behavioral spending signal"


def _build_evidence_items(
    txns: List[Dict[str, Any]],
    bayse_price: float,
    rational_prob: float,
    bias_name: str,
) -> List[BehavioralEvidence]:
    """
    Turn transactions into evidence items for the snapshot screen.
    """
    evidence: List[BehavioralEvidence] = []

    for txn in txns[:3]:
        amount = _safe_float(txn.get("amount", 0.0))
        txn_type = str(txn.get("type", "expense")).lower()
        category = str(txn.get("category", "general"))
        txn_date = txn.get("date") or txn.get("created_at") or ""

        if txn_type not in ("expense", "withdrawal", "income"):
            continue

        if txn_type == "expense" and amount < 1000:
            continue

        gap = abs(bayse_price - rational_prob)

        evidence.append(
            BehavioralEvidence(
                transaction=f"{'Spent' if txn_type == 'expense' else 'Moved'} {_format_amount(amount)}",
                date=str(txn_date),
                trigger=_detect_trigger(txn, bias_name),
                bayse_fear_at_time=round(bayse_price, 3),
                zelta_model_at_time=round(rational_prob, 3),
                gap=round(gap, 3),
                plain_english=(
                    f"Bayse crowd fear was {round(bayse_price * 100)}% "
                    f"while ZELTA's model was {round(rational_prob * 100)}%. "
                    f"This is a {round(gap * 100)}% gap."
                ),
            )
        )

    return evidence


def _build_instinct_and_math(
    free_cash: float,
    market_prob: float,
    rational_prob: float,
) -> tuple[InstinctSay, MathSay, float]:
    """
    Create the instinct-vs-math comparison.
    """
    instinct_amount = round(free_cash * market_prob, 0)
    math_amount = round(free_cash * rational_prob, 0)
    correction_value = abs(math_amount - instinct_amount)

    instinct = InstinctSay(
        action=f"Hold {_format_amount(instinct_amount)} back",
        amount=instinct_amount,
    )

    math = MathSay(
        action=f"Deploy {_format_amount(math_amount)} safely",
        amount=math_amount,
    )

    return instinct, math, correction_value


async def get_behavioral_snapshot(db: firestore.Client, uid: str) -> BehavioralSnapshot:
    """
    Build the behavioral snapshot from:
    1. Latest AI Brain output
    2. Recent wallet transactions from Firestore
    """
    # 1. Wallet summary
    wallet = await get_wallet_summary(db, uid)

    wallet_data = {
        "free_cash": _safe_float(getattr(wallet, "free_cash", 0.0)),
        "locked_total": _safe_float(getattr(wallet, "locked_total", 0.0)),
        "total_balance": _safe_float(getattr(wallet, "total_balance", 0.0)),
    }

    # 2. Run brain
    brain = await run_brain(wallet_data=wallet_data)

    bias_data = brain.get("bias", {})
    decision_data = brain.get("decision", {})
    bayse_data = brain.get("bayse", {})

    # 3. Load recent transactions
    txns = await _load_recent_transactions(db, uid)

    # 4. Use brain outputs
    bias_name = bias_data.get("active_bias", bias_data.get("bias", "Rational"))
    bias_confidence = bias_data.get("confidence", "Low")
    bias_explanation = bias_data.get("explanation", "")

    market_prob = _safe_float(decision_data.get("market_probability", 0.5), 0.5)
    rational_prob = _safe_float(decision_data.get("rational_probability", 0.5), 0.5)
    free_cash = _safe_float(wallet_data["free_cash"], 0.0)

    bayse_price = _safe_float(
        bayse_data.get("crowd_yes_price", bayse_data.get("naira_weakness_probability", 0.5)),
        0.5,
    )

    # 5. Build evidence items
    evidence = _build_evidence_items(
        txns=txns,
        bayse_price=bayse_price,
        rational_prob=rational_prob,
        bias_name=bias_name,
    )

    # 6. Build correction model
    instinct_says, math_says, correction_value = _build_instinct_and_math(
        free_cash=free_cash,
        market_prob=market_prob,
        rational_prob=rational_prob,
    )

    bayse_context = BayseContext(
        crowd_fear=round(market_prob * 100, 1),
        zelta_model=round(rational_prob * 100, 1),
        gap=round(abs(market_prob - rational_prob) * 100, 1),
        market_title=bayse_data.get("market_title", ""),
    )

    correction_plain = (
        f"Acting on data instead of panic recovers {_format_amount(correction_value)} "
        f"in opportunity cost."
    )

    return BehavioralSnapshot(
        active_bias=bias_name,
        confidence=bias_confidence,
        explanation=bias_explanation,
        evidence=evidence,
        instinct_says=instinct_says,
        math_says=math_says,
        correction_value=round(correction_value, 2),
        correction_plain=correction_plain,
        bayse_context=bayse_context,
    )
