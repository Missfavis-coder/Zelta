"""
ZELTA Side-Hustle Templates Tool
A curated catalog of campus-specific income streams for Nigerian students.
Provides structured data to help the agent suggest realistic earning paths.
"""

import logging
from typing import Dict, Any, List, Optional
from langchain_core.tools import tool

logger = logging.getLogger("zelta.tools.hustle_templates")

# ── Campus Hustle Database ──────────────────────────────────────────────────

HUSTLE_CATALOG = [
    {
        "id": "data_reselling",
        "title": "Data & Airtime Reselling",
        "barrier": "Very Low",
        "startup_ngn": 2000,
        "potential_weekly_ngn": "3,000 - 7,000",
        "tags": ["remote", "low-risk", "quick-cash"],
        "description": "Buying data in bulk from SME providers and reselling to students at a margin."
    },
    {
        "id":    "academic_support",
        "title": "Assignment & Project Assistance",
        "barrier": "High (Skill-based)",
        "startup_ngn": 0,
        "potential_weekly_ngn": "5,000 - 15,000",
        "tags": ["skill", "no-capital", "high-effort"],
        "description": "Helping peers with complex assignments, lab reports, or project documentation."
    },
    {
        "id": "pos_agent",
        "title": "Hostel POS Service",
        "barrier": "Medium",
        "startup_ngn": 15000,
        "potential_weekly_ngn": "4,000 - 10,000",
        "tags": ["physical", "reliable", "cash-flow"],
        "description": "Operating a mini-POS point in the hostel for withdrawals and transfers."
    },
    {
        "id": "tech_gig",
        "title": "Graphics Design / Web Dev Gigs",
        "barrier": "High (Skill-based)",
        "startup_ngn": 0,
        "potential_weekly_ngn": "10,000 - 40,000",
        "tags": ["skill", "remote", "high-pay"],
        "description": "Offering design or coding services to campus brands or external clients."
    },
    {
        "id": "thrift_sales",
        "title": "Campus Thrift (Okrika) Sales",
        "barrier": "Medium",
        "startup_ngn": 10000,
        "potential_weekly_ngn": "5,000 - 12,000",
        "tags": ["sales", "physical", "social"],
        "description": "Curating quality thrift wear and marketing via WhatsApp Status/Hostel groups."
    }
]

# ── Tool Implementation ──────────────────────────────────────────────────────

@tool
def get_hustle_templates(student_model: Dict[str, Any]) -> str:
    """
    Returns a list of recommended campus side-hustles based on the student's
    financial status (EMERGENCY, SURVIVAL, or NORMAL).

    Args:
        student_model: The current student_model dict from the agent state.
    """
    mode = student_model.get("agent_mode", "NORMAL")
    free_cash = student_model.get("free_cash", 0.0)

    # Filter logic based on student's current situation
    recommendations: List[Dict] = []

    for hustle in HUSTLE_CATALOG:
        # If in EMERGENCY/SURVIVAL, prioritize low startup costs
        if mode in ["EMERGENCY", "SURVIVAL"]:
            if hustle["startup_ngn"] <= (free_cash * 0.5):
                recommendations.append(hustle)
        else:
            # In NORMAL mode, show everything
            recommendations.append(hustle)

    if not recommendations:
        return "No suitable hustles found for your current budget. Focus on saving first."

    # Format output for the LLM
    output = f"### RECOMMENDED HUSTLES FOR {mode} MODE ###\n\n"
    for h in recommendations:
        output += (
            f"🔹 **{h['title']}**\n"
            f"   - Weekly Potential: ₦{h['potential_weekly_ngn']}\n"
            f"   - Startup Needed: ₦{h['startup_ngn']:,.0f}\n"
            f"   - Effort: {h['barrier']}\n"
            f"   - Summary: {h['description']}\n\n"
        )

    output += "NOTE: Advise the student to start small and prioritize school work."
    return output