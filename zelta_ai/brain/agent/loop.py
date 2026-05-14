"""
ZELTA LangGraph Agent Loop

Core agent orchestration using LangGraph StateGraph.
Routes by agent_mode (EMERGENCY/SURVIVAL/NORMAL) and wires in tools.
"""

import inspect
import logging
from typing import Dict, Any, Optional, TypedDict, Annotated, List

from langgraph.graph import StateGraph, END

try:
    # Preferred import in newer LangGraph versions
    from langgraph.graph.message import add_messages
except ImportError:  # pragma: no cover
    # Fallback for older layouts
    from langgraph.graph import add_messages  # type: ignore

from langchain_core.messages import BaseMessage

from brain.agent.student_model import build_student_model, student_model_summary
from brain.bayse.stress_signal import monitor
from brain.nlp.scraper import run_scraper
from brain.nlp.scorer import ZeltaSentimentScorer
from brain.stress.index import run_stress_index
from brain.bias.detector import ZeltaBiasDetector
from brain.bayesian.engine import run_bayesian_engine
from brain.bayesian.confidence import run_confidence_scorer
from brain.kelly.allocator import run_kelly_allocator
from brain.sharpe.scorer import ZeltaDecisionScorer
from brain.tools.hustle_templates import get_hustle_templates
from brain.tools.spending_guard import check_purchase_safety

logger = logging.getLogger("zelta.agent.loop")


# ── State Schema ─────────────────────────────────────────────────────────────

class AgentState(TypedDict, total=False):
    """Shared state for the ZELTA agent graph."""

    # Inputs
    wallet_data: Dict[str, Any]
    transactions: List[Dict[str, Any]]
    user_context: Dict[str, Any]

    # Student Model (computed first)
    student_model: Dict[str, Any]

    # Market Data
    bayse_data: Dict[str, Any]
    nlp_data: Dict[str, Any]
    stress_data: Dict[str, Any]

    # Behavioral Analysis
    bias_data: Dict[str, Any]
    bayesian_data: Dict[str, Any]
    confidence_data: Dict[str, Any]

    # Allocation
    kelly_data: Dict[str, Any]
    sharpe_data: Dict[str, Any]

    # Tool Outputs (conditional)
    hustle_recommendations: Optional[str]
    purchase_safety_check: Optional[str]

    # Final Output
    explanation: Dict[str, Any]

    # Messages for LLM / future copilot integration
    messages: Annotated[List[BaseMessage], add_messages]

    # Error handling
    error: Optional[str]


# ── Small Helpers ────────────────────────────────────────────────────────────

def _to_dict(value: Any) -> Dict[str, Any]:
    """Convert Pydantic models or dict-like objects to plain dict."""
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return {}


async def _maybe_await(value: Any) -> Any:
    """Await a value only when needed."""
    if inspect.isawaitable(value):
        return await value
    return value


def _append_error(state: AgentState, message: str) -> str:
    """Append a message to existing error text safely."""
    existing = state.get("error")
    return f"{existing}; {message}" if existing else message


async def _call_tool_or_function(obj: Any, payload: Dict[str, Any]) -> Any:
    """
    Support both LangChain-style runnables/tools with `.invoke(...)`
    and plain Python callables.
    """
    if hasattr(obj, "invoke"):
        result = obj.invoke(payload)
        return await _maybe_await(result)

    if callable(obj):
        result = obj(payload)
        return await _maybe_await(result)

    raise TypeError(f"Unsupported tool type: {type(obj)!r}")


# ── Node Functions ───────────────────────────────────────────────────────────

def build_student_model_node(state: AgentState) -> AgentState:
    """Build student survival model from inputs."""
    try:
        wallet_data = state.get("wallet_data", {})
        user_context = state.get("user_context", {})
        transactions = state.get("transactions", [])

        student_model = build_student_model(
            wallet_data=wallet_data,
            user_context=user_context,
            transactions=transactions,
        )

        logger.info(
            f"[Agent] Student model: {student_model.get('agent_mode', 'NORMAL')} | "
            f"Score: {student_model.get('survival_score', 0)}/100"
        )

        return {**state, "student_model": student_model}

    except Exception as e:
        logger.error(f"[Agent] Student model failed: {e}")
        return {**state, "error": _append_error(state, f"Student model failed: {str(e)}")}


async def fetch_market_data_node(state: AgentState) -> AgentState:
    """Fetch Bayse signal and NLP data."""
    try:
        bayse_data = monitor.get_signal() or {}

        news_payload = bayse_data.get("news_payload") or bayse_data.get("news") or []
        if not news_payload:
            try:
                news_payload = await _maybe_await(run_scraper()) or []
            except Exception:
                news_payload = []

        nlp_scorer = ZeltaSentimentScorer()
        nlp_data = _to_dict(nlp_scorer.run(news_payload))

        logger.info(
            f"[Agent] Market data fetched | Sentiment: "
            f"{nlp_data.get('aggregate_sentiment', 0):.2f}"
        )

        return {**state, "bayse_data": bayse_data, "nlp_data": nlp_data}

    except Exception as e:
        logger.error(f"[Agent] Market data fetch failed: {e}")
        return {
            **state,
            "bayse_data": {},
            "nlp_data": {"aggregate_sentiment": 0.0},
            "error": _append_error(state, f"Market data failed: {str(e)}"),
        }


def compute_stress_node(state: AgentState) -> AgentState:
    """Compute stress index from Bayse + NLP."""
    try:
        bayse_data = state.get("bayse_data", {})
        nlp_data = state.get("nlp_data", {})
        aggregate_sentiment = float(nlp_data.get("aggregate_sentiment", 0.0))

        stress_data = _to_dict(run_stress_index(bayse_data, aggregate_sentiment))

        logger.info(
            f"[Agent] Stress: {stress_data.get('score', 50)}/100 "
            f"({stress_data.get('level', 'UNKNOWN')})"
        )

        return {**state, "stress_data": stress_data}

    except Exception as e:
        logger.error(f"[Agent] Stress computation failed: {e}")
        return {
            **state,
            "stress_data": {"score": 50, "level": "UNKNOWN"},
            "error": _append_error(state, f"Stress failed: {str(e)}"),
        }


def detect_bias_node(state: AgentState) -> AgentState:
    """Detect behavioral bias."""
    try:
        stress_data = state.get("stress_data", {})
        nlp_data = state.get("nlp_data", {})
        wallet_data = state.get("wallet_data", {})
        aggregate_sentiment = float(nlp_data.get("aggregate_sentiment", 0.0))

        bias_detector = ZeltaBiasDetector()
        bias_data = _to_dict(
            bias_detector.run(stress_data, aggregate_sentiment, wallet_data)
        )

        logger.info(f"[Agent] Bias: {bias_data.get('bias', 'Rational')}")

        return {**state, "bias_data": bias_data}

    except Exception as e:
        logger.error(f"[Agent] Bias detection failed: {e}")
        return {
            **state,
            "bias_data": {"bias": "Rational", "explanation": "Bias detection failed"},
            "error": _append_error(state, f"Bias failed: {str(e)}"),
        }


def run_bayesian_node(state: AgentState) -> AgentState:
    """Run Bayesian engine to adjust crowd probability."""
    try:
        stress_data = state.get("stress_data", {})
        bias_data = state.get("bias_data", {})

        bayesian_data = _to_dict(run_bayesian_engine(stress_data, bias_data))

        logger.info(
            f"[Agent] Bayesian: {bayesian_data.get('verdict', 'HOLD')} | "
            f"Edge: {bayesian_data.get('edge', 0):.3f}"
        )

        return {**state, "bayesian_data": bayesian_data}

    except Exception as e:
        logger.error(f"[Agent] Bayesian engine failed: {e}")
        return {
            **state,
            "bayesian_data": {"verdict": "HOLD", "edge": 0.0},
            "error": _append_error(state, f"Bayesian failed: {str(e)}"),
        }


def compute_confidence_node(state: AgentState) -> AgentState:
    """Compute confidence score."""
    try:
        bayesian_data = state.get("bayesian_data", {})
        stress_data = state.get("stress_data", {})
        bias_data = state.get("bias_data", {})

        confidence_data = _to_dict(
            run_confidence_scorer(bayesian_data, stress_data, bias_data)
        )

        logger.info(
            f"[Agent] Confidence: {confidence_data.get('confidence_score_100', 0)}/100"
        )

        return {**state, "confidence_data": confidence_data}

    except Exception as e:
        logger.error(f"[Agent] Confidence scoring failed: {e}")
        return {
            **state,
            "confidence_data": {"confidence_score_100": 0, "is_actionable": False},
            "error": _append_error(state, f"Confidence failed: {str(e)}"),
        }


def run_kelly_node(state: AgentState) -> AgentState:
    """Run Kelly allocator."""
    wallet_data = state.get("wallet_data", {})
    try:
        bayesian_data = state.get("bayesian_data", {})
        confidence_data = state.get("confidence_data", {})

        kelly_data = _to_dict(
            run_kelly_allocator(bayesian_data, confidence_data, wallet_data)
        )

        logger.info(
            f"[Agent] Kelly: {kelly_data.get('verdict', 'HOLD')} | "
            f"Invest: ₦{kelly_data.get('invest_ngn', 0):,.0f}"
        )

        return {**state, "kelly_data": kelly_data}

    except Exception as e:
        logger.error(f"[Agent] Kelly allocation failed: {e}")
        return {
            **state,
            "kelly_data": {
                "verdict": "HOLD",
                "invest_ngn": 0,
                "save_ngn": 0,
                "hold_ngn": wallet_data.get("free_cash", 0),
            },
            "error": _append_error(state, f"Kelly failed: {str(e)}"),
        }


def run_sharpe_node(state: AgentState) -> AgentState:
    """Run Sharpe scorer."""
    try:
        bayesian_data = state.get("bayesian_data", {})
        sharpe_scorer = ZeltaDecisionScorer()
        sharpe_data = _to_dict(sharpe_scorer.run(bayesian_data))

        logger.info(f"[Agent] Sharpe score: {sharpe_data.get('decision_score', 0):.2f}")

        return {**state, "sharpe_data": sharpe_data}

    except Exception as e:
        logger.error(f"[Agent] Sharpe scoring failed: {e}")
        return {
            **state,
            "sharpe_data": {"decision_score": 0},
            "error": _append_error(state, f"Sharpe failed: {str(e)}"),
        }


def route_by_agent_mode(state: AgentState) -> str:
    """Route based on agent mode."""
    student_model = state.get("student_model", {})
    agent_mode = student_model.get("agent_mode", "NORMAL")

    if agent_mode == "EMERGENCY":
        return "emergency_tools"
    if agent_mode == "SURVIVAL":
        return "survival_tools"
    return "normal_analysis"


async def emergency_tools_node(state: AgentState) -> AgentState:
    """Run tools for EMERGENCY mode."""
    try:
        student_model = state.get("student_model", {})

        hustle_output = await _call_tool_or_function(
            get_hustle_templates,
            {"student_model": student_model},
        )

        safety_check = await _call_tool_or_function(
            check_purchase_safety,
            {
                "amount": student_model.get("weekly_burn_rate", 0),
                "category": "general_spending",
                "student_model": student_model,
            },
        )

        logger.info("[Agent] EMERGENCY mode: tools executed")

        return {
            **state,
            "hustle_recommendations": hustle_output,
            "purchase_safety_check": safety_check,
        }

    except Exception as e:
        logger.error(f"[Agent] Emergency tools failed: {e}")
        return {
            **state,
            "hustle_recommendations": None,
            "purchase_safety_check": "EMERGENCY: All non-essential purchases blocked.",
            "error": _append_error(state, f"Emergency tools failed: {str(e)}"),
        }


async def survival_tools_node(state: AgentState) -> AgentState:
    """Run tools for SURVIVAL mode."""
    try:
        student_model = state.get("student_model", {})

        hustle_output = await _call_tool_or_function(
            get_hustle_templates,
            {"student_model": student_model},
        )

        safety_check = await _call_tool_or_function(
            check_purchase_safety,
            {
                "amount": student_model.get("weekly_burn_rate", 0),
                "category": "general_spending",
                "student_model": student_model,
            },
        )

        logger.info("[Agent] SURVIVAL mode: tools executed")

        return {
            **state,
            "hustle_recommendations": hustle_output,
            "purchase_safety_check": safety_check,
        }

    except Exception as e:
        logger.error(f"[Agent] Survival tools failed: {e}")
        return {
            **state,
            "hustle_recommendations": None,
            "purchase_safety_check": "SURVIVAL: Use caution with purchases.",
            "error": _append_error(state, f"Survival tools failed: {str(e)}"),
        }


def normal_analysis_node(state: AgentState) -> AgentState:
    """Skip tools for NORMAL mode."""
    logger.info("[Agent] NORMAL mode: Standard analysis only")
    return {
        **state,
        "hustle_recommendations": None,
        "purchase_safety_check": None,
    }


def generate_explanation_node(state: AgentState) -> AgentState:
    """Generate final explanation."""
    explanation = {
        "summary": "Analysis complete.",
        "reasoning": "Based on student model, market signals, stress, bias, and allocation analysis.",
        "action": "See dashboard for details.",
    }

    return {**state, "explanation": explanation}


# ── Graph Construction ───────────────────────────────────────────────────────

def create_agent_graph():
    """Create the LangGraph agent."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("build_student_model", build_student_model_node)
    workflow.add_node("fetch_market_data", fetch_market_data_node)
    workflow.add_node("compute_stress", compute_stress_node)
    workflow.add_node("detect_bias", detect_bias_node)
    workflow.add_node("run_bayesian", run_bayesian_node)
    workflow.add_node("compute_confidence", compute_confidence_node)
    workflow.add_node("run_kelly", run_kelly_node)
    workflow.add_node("run_sharpe", run_sharpe_node)
    workflow.add_node("emergency_tools", emergency_tools_node)
    workflow.add_node("survival_tools", survival_tools_node)
    workflow.add_node("normal_analysis", normal_analysis_node)
    workflow.add_node("generate_explanation", generate_explanation_node)

    # Set entry point
    workflow.set_entry_point("build_student_model")

    # Linear analysis flow
    workflow.add_edge("build_student_model", "fetch_market_data")
    workflow.add_edge("fetch_market_data", "compute_stress")
    workflow.add_edge("compute_stress", "detect_bias")
    workflow.add_edge("detect_bias", "run_bayesian")
    workflow.add_edge("run_bayesian", "compute_confidence")
    workflow.add_edge("compute_confidence", "run_kelly")
    workflow.add_edge("run_kelly", "run_sharpe")

    # Conditional routing based on agent mode
    workflow.add_conditional_edges(
        "run_sharpe",
        route_by_agent_mode,
        {
            "emergency_tools": "emergency_tools",
            "survival_tools": "survival_tools",
            "normal_analysis": "normal_analysis",
        },
    )

    # Converge to explanation
    workflow.add_edge("emergency_tools", "generate_explanation")
    workflow.add_edge("survival_tools", "generate_explanation")
    workflow.add_edge("normal_analysis", "generate_explanation")

    # End
    workflow.add_edge("generate_explanation", END)

    return workflow.compile()


# ── Main Entry Point ─────────────────────────────────────────────────────────

async def run_agent(
    wallet_data: Dict[str, Any],
    transactions: List[Dict[str, Any]],
    user_context: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Run the ZELTA agent graph.

    Args:
        wallet_data: User wallet data
        transactions: Transaction history
        user_context: User profile and context

    Returns:
        Complete agent state with all analysis results
    """
    try:
        graph = create_agent_graph()

        initial_state: AgentState = {
            "wallet_data": wallet_data,
            "transactions": transactions,
            "user_context": user_context,
            "student_model": {},
            "bayse_data": {},
            "nlp_data": {},
            "stress_data": {},
            "bias_data": {},
            "bayesian_data": {},
            "confidence_data": {},
            "kelly_data": {},
            "sharpe_data": {},
            "hustle_recommendations": None,
            "purchase_safety_check": None,
            "explanation": {},
            "messages": [],
            "error": None,
        }

        final_state = await graph.ainvoke(initial_state)

        response = {
            "meta": {
                "status": "error" if final_state.get("error") else "success",
                "error": final_state.get("error"),
            },
            "student_model": final_state.get("student_model", {}),
            "bayse": final_state.get("bayse_data", {}),
            "nlp": final_state.get("nlp_data", {}),
            "stress": final_state.get("stress_data", {}),
            "bias": final_state.get("bias_data", {}),
            "decision": final_state.get("bayesian_data", {}),
            "confidence": final_state.get("confidence_data", {}),
            "allocation": final_state.get("kelly_data", {}),
            "score": final_state.get("sharpe_data", {}),
            "explanation": final_state.get("explanation", {}),
            "hustle_recommendations": final_state.get("hustle_recommendations"),
            "purchase_safety_check": final_state.get("purchase_safety_check"),
        }

        return response

    except Exception as e:
        logger.error(f"[Agent] Graph execution failed: {e}")
        return {
            "meta": {
                "status": "error",
                "error": str(e),
            }
        }