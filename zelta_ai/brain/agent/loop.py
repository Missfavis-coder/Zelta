"""
ZELTA LangGraph Agent Loop

Core agent orchestration using LangGraph StateGraph.
Routes by agent_mode (EMERGENCY/SURVIVAL/NORMAL) and wires in tools.
"""

import logging
from typing import Dict, Any, Optional, TypedDict, Annotated, List
from operator import add

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

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

class AgentState(TypedDict):
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
    
    # Messages for LLM
    messages: Annotated[List[Dict[str, Any]], add]
    
    # Error handling
    error: Optional[str]


# ── Node Functions ───────────────────────────────────────────────────────────

def _to_dict(value: Any) -> Dict[str, Any]:
    """Convert Pydantic models or dicts to plain dict."""
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return {}


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
        
        logger.info(f"[Agent] Student model: {student_model['agent_mode']} | Score: {student_model['survival_score']}/100")
        
        return {**state, "student_model": student_model}
    except Exception as e:
        logger.error(f"[Agent] Student model failed: {e}")
        return {**state, "error": f"Student model failed: {str(e)}"}


def fetch_market_data_node(state: AgentState) -> AgentState:
    """Fetch Bayse signal and NLP data."""
    try:
        # 1. Bayse signal (primary)
        bayse_data = monitor.get_signal() or {}
        
        # 2. NLP data
        news_payload = bayse_data.get("news_payload") or bayse_data.get("news") or []
        if not news_payload:
            try:
                import asyncio
                news_payload = asyncio.run(run_scraper()) or []
            except:
                news_payload = []
        
        nlp_scorer = ZeltaSentimentScorer()
        nlp_data = _to_dict(nlp_scorer.run(news_payload))
        
        logger.info(f"[Agent] Market data fetched | Sentiment: {nlp_data.get('aggregate_sentiment', 0):.2f}")
        
        return {**state, "bayse_data": bayse_data, "nlp_data": nlp_data}
    except Exception as e:
        logger.error(f"[Agent] Market data fetch failed: {e}")
        # Return defaults to not block the pipeline
        return {
            **state,
            "bayse_data": {},
            "nlp_data": {"aggregate_sentiment": 0.0},
            "error": state.get("error") + f"; Market data failed: {str(e)}" if state.get("error") else f"Market data failed: {str(e)}"
        }


def compute_stress_node(state: AgentState) -> AgentState:
    """Compute stress index from Bayse + NLP."""
    try:
        bayse_data = state.get("bayse_data", {})
        nlp_data = state.get("nlp_data", {})
        aggregate_sentiment = float(nlp_data.get("aggregate_sentiment", 0.0))
        
        stress_data = _to_dict(run_stress_index(bayse_data, aggregate_sentiment))
        
        logger.info(f"[Agent] Stress: {stress_data.get('score', 50)}/100 ({stress_data.get('level', 'UNKNOWN')})")
        
        return {**state, "stress_data": stress_data}
    except Exception as e:
        logger.error(f"[Agent] Stress computation failed: {e}")
        return {
            **state,
            "stress_data": {"score": 50, "level": "UNKNOWN"},
            "error": state.get("error") + f"; Stress failed: {str(e)}" if state.get("error") else f"Stress failed: {str(e)}"
        }


def detect_bias_node(state: AgentState) -> AgentState:
    """Detect behavioral bias."""
    try:
        stress_data = state.get("stress_data", {})
        nlp_data = state.get("nlp_data", {})
        wallet_data = state.get("wallet_data", {})
        aggregate_sentiment = float(nlp_data.get("aggregate_sentiment", 0.0))
        
        bias_detector = ZeltaBiasDetector()
        bias_data = _to_dict(bias_detector.run(stress_data, aggregate_sentiment, wallet_data))
        
        logger.info(f"[Agent] Bias: {bias_data.get('bias', 'Rational')}")
        
        return {**state, "bias_data": bias_data}
    except Exception as e:
        logger.error(f"[Agent] Bias detection failed: {e}")
        return {
            **state,
            "bias_data": {"bias": "Rational", "explanation": "Bias detection failed"},
            "error": state.get("error") + f"; Bias failed: {str(e)}" if state.get("error") else f"Bias failed: {str(e)}"
        }


def run_bayesian_node(state: AgentState) -> AgentState:
    """Run Bayesian engine to adjust crowd probability."""
    try:
        stress_data = state.get("stress_data", {})
        bias_data = state.get("bias_data", {})
        
        bayesian_data = _to_dict(run_bayesian_engine(stress_data, bias_data))
        
        logger.info(f"[Agent] Bayesian: {bayesian_data.get('verdict', 'HOLD')} | Edge: {bayesian_data.get('edge', 0):.3f}")
        
        return {**state, "bayesian_data": bayesian_data}
    except Exception as e:
        logger.error(f"[Agent] Bayesian engine failed: {e}")
        return {
            **state,
            "bayesian_data": {"verdict": "HOLD", "edge": 0.0},
            "error": state.get("error") + f"; Bayesian failed: {str(e)}" if state.get("error") else f"Bayesian failed: {str(e)}"
        }


def compute_confidence_node(state: AgentState) -> AgentState:
    """Compute confidence score."""
    try:
        bayesian_data = state.get("bayesian_data", {})
        stress_data = state.get("stress_data", {})
        bias_data = state.get("bias_data", {})
        
        confidence_data = _to_dict(run_confidence_scorer(bayesian_data, stress_data, bias_data))
        
        logger.info(f"[Agent] Confidence: {confidence_data.get('confidence_score_100', 0)}/100")
        
        return {**state, "confidence_data": confidence_data}
    except Exception as e:
        logger.error(f"[Agent] Confidence scoring failed: {e}")
        return {
            **state,
            "confidence_data": {"confidence_score_100": 0, "is_actionable": False},
            "error": state.get("error") + f"; Confidence failed: {str(e)}" if state.get("error") else f"Confidence failed: {str(e)}"
        }


def run_kelly_node(state: AgentState) -> AgentState:
    """Run Kelly allocator."""
    try:
        bayesian_data = state.get("bayesian_data", {})
        confidence_data = state.get("confidence_data", {})
        wallet_data = state.get("wallet_data", {})
        
        kelly_data = _to_dict(run_kelly_allocator(bayesian_data, confidence_data, wallet_data))
        
        logger.info(f"[Agent] Kelly: {kelly_data.get('verdict', 'HOLD')} | Invest: ₦{kelly_data.get('invest_ngn', 0):,.0f}")
        
        return {**state, "kelly_data": kelly_data}
    except Exception as e:
        logger.error(f"[Agent] Kelly allocation failed: {e}")
        return {
            **state,
            "kelly_data": {"verdict": "HOLD", "invest_ngn": 0, "save_ngn": 0, "hold_ngn": wallet_data.get("free_cash", 0)},
            "error": state.get("error") + f"; Kelly failed: {str(e)}" if state.get("error") else f"Kelly failed: {str(e)}"
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
            "error": state.get("error") + f"; Sharpe failed: {str(e)}" if state.get("error") else f"Sharpe failed: {str(e)}"
        }


def route_by_agent_mode(state: AgentState) -> str:
    """Route based on agent mode."""
    student_model = state.get("student_model", {})
    agent_mode = student_model.get("agent_mode", "NORMAL")
    
    if agent_mode == "EMERGENCY":
        return "emergency_tools"
    elif agent_mode == "SURVIVAL":
        return "survival_tools"
    else:
        return "normal_analysis"


def emergency_tools_node(state: AgentState) -> AgentState:
    """Run tools for EMERGENCY mode."""
    try:
        student_model = state.get("student_model", {})
        
        # Get hustle recommendations
        hustle_output = get_hustle_templates.invoke({"student_model": student_model})
        
        logger.info(f"[Agent] EMERGENCY mode: Hustle recommendations generated")
        
        return {
            **state,
            "hustle_recommendations": hustle_output,
            "purchase_safety_check": "EMERGENCY: All non-essential purchases blocked."
        }
    except Exception as e:
        logger.error(f"[Agent] Emergency tools failed: {e}")
        return {
            **state,
            "hustle_recommendations": None,
            "error": state.get("error") + f"; Emergency tools failed: {str(e)}" if state.get("error") else f"Emergency tools failed: {str(e)}"
        }


def survival_tools_node(state: AgentState) -> AgentState:
    """Run tools for SURVIVAL mode."""
    try:
        student_model = state.get("student_model", {})
        
        # Get hustle recommendations
        hustle_output = get_hustle_templates.invoke({"student_model": student_model})
        
        logger.info(f"[Agent] SURVIVAL mode: Hustle recommendations generated")
        
        return {
            **state,
            "hustle_recommendations": hustle_output,
            "purchase_safety_check": "SURVIVAL: Use caution with purchases."
        }
    except Exception as e:
        logger.error(f"[Agent] Survival tools failed: {e}")
        return {
            **state,
            "hustle_recommendations": None,
            "error": state.get("error") + f"; Survival tools failed: {str(e)}" if state.get("error") else f"Survival tools failed: {str(e)}"
        }


def normal_analysis_node(state: AgentState) -> AgentState:
    """Skip tools for NORMAL mode."""
    logger.info(f"[Agent] NORMAL mode: Standard analysis only")
    return {
        **state,
        "hustle_recommendations": None,
        "purchase_safety_check": None
    }


def generate_explanation_node(state: AgentState) -> AgentState:
    """Generate final explanation (placeholder - will be updated with LangChain copilot)."""
    # This node will be replaced with the updated copilot
    # For now, return a basic explanation
    explanation = {
        "summary": "Analysis complete.",
        "reasoning": "Based on market data and student model.",
        "action": "See dashboard for details.",
    }
    
    return {**state, "explanation": explanation}


# ── Graph Construction ───────────────────────────────────────────────────────

def create_agent_graph() -> StateGraph:
    """Create the LangGraph agent."""
    
    # Create the graph
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
    
    # Add edges (linear flow for analysis)
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
        }
    )
    
    # All paths converge to explanation
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
        # Create the graph
        graph = create_agent_graph()
        
        # Initial state
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
        
        # Run the graph
        final_state = await graph.ainvoke(initial_state)
        
        # Build response (maintain backward compatibility with pipeline.py output)
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
            # Tool outputs
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
