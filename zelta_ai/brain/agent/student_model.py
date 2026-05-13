"""
ZELTA Student Survival Model

Transforms raw wallet + profile data into a single student_model dict
that every agent component reads from. This is the single source of
truth for "is this student okay right now?"

No LangChain here — pure deterministic Python.
The LangGraph agent and all tools import from here.
"""

from __future__ import annotations

import logging
import statistics
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger("zelta.agent.student_model")

# ── Constants ────────────────────────────────────────────────────────────────

# Minimum weekly buffer for absolute essentials (food + transport + data)
MINIMUM_WEEKLY_BUFFER_NGN: float = 4000.0  # Updated for 2026 inflation

# Fee deadline is "imminent" if within this many weeks
FEE_IMMINENT_WEEKS: int = 8

# Emergency mode threshold
EMERGENCY_RUNWAY_WEEKS: float = 2.0


# ── Internal helpers ─────────────────────────────────────────────────────────

def _safe_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(val) if val is not None else default
    except (TypeError, ValueError):
        return default


def _parse_iso(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        try:
            # Handle Zulu time and standard offsets
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return None


def _compute_robust_burn(transactions: List[Dict[str, Any]]) -> float:
    """
    Computes a robust weekly burn by filtering out outliers
    (one-time big purchases like hostel fees or equipment).
    """
    expenses = [
        _safe_float(t.get("amount"))
        for t in transactions
        if t.get("type") == "expense" and _safe_float(t.get("amount")) > 0
    ]

    if not expenses:
        return 0.0

    if len(expenses) < 3:
        return sum(expenses) / max(len(expenses), 1)

    # Statistical Outlier Filtering (2 Standard Deviations)
    # Prevents a single tuition payment from making the agent think
    # the student's weekly lifestyle costs ₦200k.
    mean = statistics.mean(expenses)
    stdev = statistics.stdev(expenses)
    filtered = [e for e in expenses if e <= (mean + 2 * stdev)]

    # Return the sum of the last 7 filtered transactions as a proxy for weekly burn
    return sum(filtered[-7:]) if filtered else mean


# ── Public API ────────────────────────────────────────────────────────────────

def build_student_model(
    wallet_data: Dict[str, Any],
    user_context: Dict[str, Any],
    transactions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Build the student survival model from wallet + profile data.
    """
    transactions = transactions or []

    # 1. Wallet Basics
    free_cash = _safe_float(wallet_data.get("free_cash"))
    locked_total = _safe_float(wallet_data.get("locked_total"))
    total_balance = _safe_float(wallet_data.get("total_balance", free_cash + locked_total))

    # 2. Profile & Financial Context
    financial = user_context.get("financial") or {}
    weekly_allowance = _safe_float(
        financial.get("weekly_allowance") or (financial.get("monthly_income", 0) / 4)
    )

    # 3. Fee Obligations Logic
    fee_obligations = financial.get("fee_obligations") or []
    now = datetime.now(timezone.utc)
    weeks_to_fee, fee_amount = 999.0, 0.0

    for obl in fee_obligations:
        due = _parse_iso(obl.get("due_date"))
        if due:
            weeks = max(0, (due - now).days / 7)
            if weeks < weeks_to_fee:
                weeks_to_fee, fee_amount = weeks, _safe_float(obl.get("amount"))

    # Fallback for raw tuition/hostel values
    if fee_amount == 0.0:
        raw_fees = _safe_float(financial.get("tuition_amount", 0)) + _safe_float(financial.get("hostel_fee", 0))
        if raw_fees > 0:
            fee_amount, weeks_to_fee = raw_fees, 8.0

    # 4. Burn Rate & Runway
    weekly_burn = _compute_robust_burn(transactions)
    if weekly_burn == 0:
        weekly_burn = free_cash * 0.15 # Fallback: 15% weekly burn estimate

    weeks_of_runway = free_cash / weekly_burn if weekly_burn > 0 else 999.0

    # 5. Gap & Savings Requirements
    fee_gap_ngn = max(0.0, fee_amount - free_cash)
    weekly_saving_needed = (fee_gap_ngn / max(weeks_to_fee, 1)) if fee_gap_ngn > 0 else 0.0

    # 6. Safe Discretionary Spending
    # Allowance - Savings Requirement - Survival Buffer
    safe_discretionary = max(0.0, weekly_allowance - weekly_saving_needed - MINIMUM_WEEKLY_BUFFER_NGN)

    # 7. Survival State Detection
    emergency_mode = weeks_of_runway < EMERGENCY_RUNWAY_WEEKS
    fee_is_imminent = weeks_to_fee < FEE_IMMINENT_WEEKS
    student_will_miss_fee = fee_is_imminent and (weeks_of_runway < weeks_to_fee) and fee_amount > 0
    survival_mode = emergency_mode or student_will_miss_fee

    agent_mode = "EMERGENCY" if emergency_mode else ("SURVIVAL" if survival_mode else "NORMAL")

    # 8. Survival Score (0-100)
    if emergency_mode:
        survival_score = max(0, min(20, int(weeks_of_runway * 10)))
    elif student_will_miss_fee:
        covered_ratio = min(1.0, free_cash / max(fee_amount, 1.0))
        survival_score = int(covered_ratio * 60)
    else:
        runway_ratio = min(1.0, weeks_of_runway / max(weeks_to_fee, 1.0)) if weeks_to_fee < 999 else 1.0
        survival_score = 60 + int(runway_ratio * 40)

    # 9. Behavioral Context (Agent Perception Layer)
    behavioral = {
        "stress_level": "CRITICAL" if emergency_mode else ("HIGH" if student_will_miss_fee else "STABLE"),
        "primary_directive": (
            "Halt all non-essential spending. Focus on immediate survival." if emergency_mode else
            f"Prioritize saving ₦{weekly_saving_needed:,.0f}/week for upcoming fees." if student_will_miss_fee else
            "Encourage smart micro-investing and sustainable spending."
        )
    }

    # 10. Status Message
    if emergency_mode:
        status_message = f"⚠️ Money runs out in {weeks_of_runway:.1f} weeks. Cut all non-essentials."
    elif student_will_miss_fee:
        status_message = f"Fee gap: ₦{fee_gap_ngn:,.0f}. Save ₦{weekly_saving_needed:,.0f}/week to hit deadline."
    else:
        status_message = f"On track. Safe weekly spend: ₦{safe_discretionary:,.0f}."

    return {
        "agent_mode": agent_mode,
        "survival_score": survival_score,
        "free_cash": free_cash,
        "weeks_of_runway": round(weeks_of_runway, 1),
        "weeks_to_fee_deadline": round(weeks_to_fee, 1),
        "fee_amount_due": fee_amount,
        "fee_gap_ngn": fee_gap_ngn,
        "weekly_burn_rate": round(weekly_burn, 2),
        "safe_discretionary_ngn": round(safe_discretionary, 2),
        "survival_mode": survival_mode,
        "emergency_mode": emergency_mode,
        "behavioral": behavioral,
        "status_message": status_message,
        "risk_tolerance": financial.get("risk_tolerance", "low"),
    }


def student_model_summary(model: Dict[str, Any]) -> str:
    """
    Compact summary for prompt injection.
    """
    return (
        f"[{model['agent_mode']}] Score: {model['survival_score']}/100 | "
        f"Runway: {model['weeks_of_runway']}wk | "
        f"Safe Spend: ₦{model['safe_discretionary_ngn']:,.0f}/wk | "
        f"Directive: {model['behavioral']['primary_directive']}"
    )