"""
ZELTA Behavioral Service

This service powers:
1. Behavioral Snapshot
   - Why ZELTA flagged the user's current behavior as irrational
   - Uses latest AI Brain output + recent wallet transactions

2. Behavioral Pattern
   - 8-week behavioral trend screen
   - Uses decision history from Firestore

This service does NOT run the full pipeline in the frontend.
It only prepares human-readable behavioral explanations.
"""

import logging
from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Tuple

from google.cloud import firestore

from optimizer import run_brain
from services.wallet_service import get_wallet_summary
from schemas.behavioral import (
    BehavioralBiasCard,
    BehavioralEvidence,
    BehavioralPattern,
    BehavioralWeekItem,
    BehavioralSnapshot,
    InstinctSay,
    MathSay,
)

logger = logging.getLogger(__name__)

BEHAVIORAL_BIASES = [
    "Loss Aversion",
    "Present Bias",
    "Overconfidence",
    "Herd Behavior",
    "Mental Accounting",
]


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


def _to_datetime(value: Any) -> datetime | None:
    """
    Convert Firestore timestamps / ISO strings / datetimes into datetime.
    """
    if value is None:
        return None

    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    try:
        if hasattr(value, "to_datetime"):
            dt = value.to_datetime()
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt
    except Exception:
        pass

    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except Exception:
        return None


def _get_transactions_ref(db: firestore.Client, uid: str):
    return (
        db.collection("users")
        .document(uid)
        .collection("transactions")
        .order_by("date", direction=firestore.Query.DESCENDING)
        .limit(10)
    )


def _get_decisions_ref(db: firestore.Client, uid: str):
    return (
        db.collection("portfolio")
        .document(uid)
        .collection("decisions")
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(100)
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


async def _load_recent_decisions(db: firestore.Client, uid: str) -> List[Dict[str, Any]]:
    """
    Load recent portfolio decisions from Firestore.
    """
    try:
        docs = _get_decisions_ref(db, uid).stream()
        return [doc.to_dict() for doc in docs if doc.to_dict()]
    except Exception as exc:
        logger.exception("Failed to load recent decisions: %s", exc)
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

    for txn in txns[:5]:
        amount = _safe_float(txn.get("amount", 0.0))
        txn_type = str(txn.get("type", "expense")).lower()
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
) -> Tuple[InstinctSay, MathSay, float]:
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


def _build_bias_cards(
    bias_name: str,
    recent_decisions: List[Dict[str, Any]],
) -> Tuple[List[BehavioralBiasCard], float, str]:
    """
    Build the five bias cards shown on the behavioral screen.

    Strength is estimated from recent decision history.
    """
    total = max(1, len(recent_decisions))
    bias_counts = Counter()

    for d in recent_decisions:
        recorded_bias = (
            d.get("bias_at_decision")
            or d.get("bias")
            or d.get("active_bias")
            or "Rational"
        )
        bias_counts[str(recorded_bias)] += 1

    cards: List[BehavioralBiasCard] = []
    active_strength = 0.0

    for b in BEHAVIORAL_BIASES:
        count = bias_counts.get(b, 0)
        strength = round((count / total) * 100, 1) if total > 0 else 0.0

        if strength >= 70:
            status = "HIGH"
        elif strength >= 40:
            status = "MODERATE"
        else:
            status = "LOW"

        if b == bias_name:
            status = "ACTIVE"
            active_strength = max(active_strength, strength)

        explanation = {
            "Loss Aversion": "Prioritizing avoiding losses over potential gains during Bayse fear spikes.",
            "Present Bias": "Tendency to prefer immediate rewards over delayed benefits.",
            "Overconfidence": "Overestimating ability to predict outcomes when stress is low.",
            "Herd Behavior": "Following peer decisions without independent analysis.",
            "Mental Accounting": "Treating money differently based on source.",
        }.get(b, "")

        cards.append(
            BehavioralBiasCard(
                bias=b,
                status=status,
                current_strength=strength,
                explanation=explanation,
            )
        )

    if active_strength == 0.0:
        active_strength = max(
            (card.current_strength for card in cards if card.bias == bias_name),
            default=0.0,
        )

    strength_label = (
        "HIGH" if active_strength >= 70 else "MODERATE" if active_strength >= 40 else "LOW"
    )

    return cards, active_strength, strength_label


def _bias_to_week_strength(decision_score: float) -> float:
    """
    Convert decision score into a readable weekly strength percentage.
    """
    return max(0.0, min(100.0, round(decision_score * 20.0, 1)))


def _bias_from_decision(doc: Dict[str, Any]) -> str:
    """
    Extract bias from a decision record.
    """
    return (
        doc.get("bias_at_decision")
        or doc.get("bias")
        or doc.get("active_bias")
        or "None"
    )


def _classify_bias_for_week(bias_name: str, strength: float) -> str:
    """
    Decide whether a week should display a named bias or None.
    """
    if strength < 20:
        return "None"
    return bias_name


def _week_label_for(dt: datetime) -> str:
    return dt.strftime("Week %V")


async def get_behavioral_snapshot(db: firestore.Client, uid: str) -> BehavioralSnapshot:
    """
    Build the behavioral snapshot from:
    1. Latest AI Brain output
    2. Recent wallet transactions from Firestore
    3. Recent portfolio decisions for bias context
    """
    wallet = await get_wallet_summary(db, uid)

    wallet_data = {
        "free_cash": _safe_float(getattr(wallet, "free_cash", 0.0)),
        "locked_total": _safe_float(getattr(wallet, "locked_total", 0.0)),
        "total_balance": _safe_float(getattr(wallet, "total_balance", 0.0)),
    }

    brain = await run_brain(wallet_data=wallet_data)

    bias_data = brain.get("bias", {})
    decision_data = brain.get("decision", {})
    bayse_data = brain.get("bayse", {})
    confidence_data = brain.get("confidence", {})

    txns = await _load_recent_transactions(db, uid)
    decisions = await _load_recent_decisions(db, uid)

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

    evidence = _build_evidence_items(
        txns=txns,
        bayse_price=bayse_price,
        rational_prob=rational_prob,
        bias_name=bias_name,
    )

    instinct_says, math_says, correction_value = _build_instinct_and_math(
        free_cash=free_cash,
        market_prob=market_prob,
        rational_prob=rational_prob,
    )

    rational_pct = _safe_float(confidence_data.get("rational_pct", round(rational_prob * 100, 1)))
    behavioral_pct = _safe_float(confidence_data.get("behavioral_pct", 100.0 - rational_pct))
    decision_gap = _safe_float(confidence_data.get("gap", abs(rational_pct - behavioral_pct)))
    confidence_score = _safe_float(
        confidence_data.get("confidence_score_100", confidence_data.get("confidence_score", 0.0))
    )
    confidence_tier = confidence_data.get("confidence_tier", "Low")
    intervention_urgency = confidence_data.get("intervention_urgency", "MODERATE")
    decision_plain = confidence_data.get("plain_english", "")

    tracked_biases, active_bias_strength, bias_strength_label = _build_bias_cards(
        bias_name=bias_name,
        recent_decisions=decisions,
    )

    correction_plain = (
        f"Acting on data instead of panic recovers {_format_amount(correction_value)} "
        f"in opportunity cost."
    )

    recommendation = (
        f"Your {bias_name.lower()} is being triggered by Bayse crowd fear spikes that don't match actual risk. "
        f"When Bayse signals go above 70%, wait 24 hours before making cash withdrawal decisions. "
        f"The crowd panic typically corrects within 48 hours."
    )

    return BehavioralSnapshot(
        active_bias=bias_name,
        confidence=bias_confidence,
        explanation=bias_explanation,
        bayse_crowd_fear=round(market_prob * 100, 1),
        bayse_zelta_model=round(rational_prob * 100, 1),
        bayse_gap=round(abs(market_prob - rational_prob) * 100, 1),
        bayse_market_title=bayse_data.get("market_title", ""),
        rational_pct=round(rational_pct, 1),
        behavioral_pct=round(behavioral_pct, 1),
        decision_gap=round(decision_gap, 1),
        confidence_score=round(confidence_score, 1),
        confidence_tier=confidence_tier,
        intervention_urgency=intervention_urgency,
        decision_plain_english=decision_plain,
        bias_strength_label=bias_strength_label,
        bias_strength_value=round(active_bias_strength, 1),
        evidence=evidence,
        tracked_biases=tracked_biases,
        instinct_says=instinct_says,
        math_says=math_says,
        correction_value=round(correction_value, 2),
        correction_plain=correction_plain,
        recommendation=recommendation,
    )


async def get_behavioral_pattern(db: firestore.Client, uid: str) -> BehavioralPattern:
    """
    Build the 8-week behavioral pattern from decision history in Firestore.
    """
    decisions = await _load_recent_decisions(db, uid)

    if not decisions:
        return BehavioralPattern(
            weeks=[],
            dominant_bias="None",
            summary="No behavioral history yet. Start saving decisions to build your pattern.",
            recommendation="Keep logging ZELTA recommendations so your behavioral pattern can be tracked.",
            confidence_gap=0.0,
        )

    timed_decisions: List[Tuple[datetime, Dict[str, Any]]] = []
    for d in decisions:
        dt = _to_datetime(d.get("created_at") or d.get("resolved_at"))
        if dt is not None:
            timed_decisions.append((dt, d))

    timed_decisions.sort(key=lambda item: item[0])

    if timed_decisions:
        latest_dt = timed_decisions[-1][0]
    else:
        latest_dt = datetime.now(timezone.utc)

    week_starts: List[datetime] = []
    current_start = latest_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    current_start = current_start - timedelta(days=current_start.weekday())

    for i in range(7, -1, -1):
        week_starts.append(current_start - timedelta(weeks=i))

    week_buckets: List[BehavioralWeekItem] = []

    for start in week_starts:
        end = start + timedelta(days=7)
        bucket = [d for dt, d in timed_decisions if start <= dt < end]

        if not bucket:
            week_buckets.append(
                BehavioralWeekItem(
                    week=_week_label_for(start),
                    bias="None",
                    strength=10.0,
                    note="No strong signal this week.",
                    confidence_label="LOW",
                )
            )
            continue

        bias_counter = Counter()
        score_values: List[float] = []

        for doc in bucket:
            bias_name = _bias_from_decision(doc)
            if bias_name and bias_name != "Rational":
                bias_counter[bias_name] += 1
            score_values.append(_safe_float(doc.get("decision_score", 0.0)))

        dominant_bias = bias_counter.most_common(1)[0][0] if bias_counter else "None"
        avg_score = sum(score_values) / max(1, len(score_values))
        strength = _bias_to_week_strength(avg_score)
        display_bias = _classify_bias_for_week(dominant_bias, strength)

        if strength >= 70:
            confidence_label = "HIGH"
        elif strength >= 40:
            confidence_label = "MODERATE"
        else:
            confidence_label = "LOW"

        if display_bias == "None":
            note = "No strong behavioral bias detected."
        else:
            note = f"{display_bias} was the dominant pattern this week."

        week_buckets.append(
            BehavioralWeekItem(
                week=_week_label_for(start),
                bias=display_bias,
                strength=round(strength, 1),
                note=note,
                confidence_label=confidence_label,
            )
        )

    all_biases = Counter(
        _bias_from_decision(d)
        for _, d in timed_decisions
        if _bias_from_decision(d) != "Rational"
    )
    dominant_bias = all_biases.most_common(1)[0][0] if all_biases else "None"

    total_decisions = len(timed_decisions)
    confidence_gap = 0.0
    if total_decisions > 0:
        high_bias_count = sum(
            1 for _, d in timed_decisions
            if _bias_from_decision(d) != "Rational"
        )
        confidence_gap = round((high_bias_count / total_decisions) * 100, 1)

    summary = (
        f"Over the last 8 weeks, {dominant_bias.replace('_', ' ').title()} "
        f"appeared most often in your decisions."
    )

    recommendation = (
        f"Your {dominant_bias.lower() if dominant_bias != 'None' else 'behavior'} is being triggered by Bayse fear spikes that don't always match real risk. "
        f"When Bayse signals are high, slow down before moving cash."
    )

    return BehavioralPattern(
        weeks=week_buckets,
        dominant_bias=dominant_bias,
        summary=summary,
        recommendation=recommendation,
        confidence_gap=confidence_gap,
    )
