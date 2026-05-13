"""
ZELTA Spending Guard Tool
The first LangChain-integrated component.
Provides a "Safe/Unsafe" verdict for proposed purchases.
"""
import logging
from typing import Dict, Any
from langchain_core.tools import tool

logger = logging.getLogger("zelta.tools.spending_guard")

@tool
def check_purchase_safety(amount: float, category: str, student_model: Dict[str, Any]) -> str:
    """
    Evaluates if a proposed purchase is safe based on the student's current survival metrics.

    Args:
        amount: The cost of the item in NGN (Naira)
        category: The type of purchase (e.g., 'Food', 'Electronics', 'Entertainment').
        student_model: The current student_model dictionary from the agent state.
    """
    # Extract core limits from the model
    safe_limit = student_model.get("safe_discretionary_ngn", 0.0)
    mode = student_model.get("agent_mode", "NORMAL")
    runway = student_model.get("weeks_of_runway", 0.0)
    # Logic: The Verdict
    if mode == "EMERGENCY":
        return (
            f"❌ VERDICT: BLOCKED. You are in EMERGENCY mode with only {runway} weeks of runway. "
            f"Spending ₦{amount:,.0f} on {category} is highly risky. Stick to absolute essentials only."
        )

    if mode == "SURVIVAL":
        if amount > (safe_limit * 0.5):  # Survival mode allows only half of the "safe" spend for extra safety
            return (
                f"⚠️ VERDICT: RISKY. You are in SURVIVAL mode. This ₦{amount:,.0f} purchase "
                f"exceeds the cautious limit for your current fee-saving goals."
            )
        return (
            f"✅ VERDICT: CAUTIOUS PASS. While you are in SURVIVAL mode, ₦{amount:,.0f} is within "
            f"a manageable range, provided you cut back elsewhere this week."
        )
    # 3. Normal Mode Logic
    if amount <= safe_limit:
        return (
            f"✅ VERDICT: SAFE. ₦{amount:,.0f} is within your weekly safe spending limit "
            f"of ₦{safe_limit:,.0f}. Enjoy your {category}!"
        )
    else:
        diff = amount - safe_limit
        return (
            f"⚠️ VERDICT: OVER LIMIT. This purchase is ₦{diff:,.0f} over your safe weekly limit. "
            f"If you buy this, you'll need to reduce spending by that amount next week to stay on track."
        )
