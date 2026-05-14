import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

from brain.agent.loop import run_agent
from brain.copilot.gemini import ZeltaCopilot

logger = logging.getLogger("zelta.pipeline")


def _to_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return {}


class ZeltaPipeline:
    """
    Central AI Brain Orchestrator (QUELO)

    Now uses LangGraph agent for orchestration instead of sequential execution.
    Flow:
    Input → Student Model → Agent Mode Router → Analysis Nodes → Copilot → Output
    """

    def __init__(self):
        self.copilot = ZeltaCopilot()

    def _validate_wallet(self, wallet_data: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """
        Ensure wallet is always valid (comes from USER).
        Supports both locked_total and locked_amount for compatibility.
        Validates against missing keys, zero cash, negative values, and bad defaults.
        """
        if not wallet_data:
            logger.warning("[Pipeline] No wallet data provided, using safe defaults")
            return {
                "free_cash": 10000.0,
                "locked_total": 0.0,
                "total_balance": 10000.0,
            }

        # Extract and validate values
        free_cash = wallet_data.get("free_cash", 0.0)
        locked_value = wallet_data.get("locked_total", wallet_data.get("locked_amount", 0.0))
        total_balance = wallet_data.get("total_balance", 0.0)

        # Convert to float and validate
        try:
            free_cash = float(free_cash)
        except (TypeError, ValueError):
            logger.warning("[Pipeline] Invalid free_cash, defaulting to 0")
            free_cash = 0.0

        try:
            locked_value = float(locked_value)
        except (TypeError, ValueError):
            logger.warning("[Pipeline] Invalid locked_total, defaulting to 0")
            locked_value = 0.0

        try:
            total_balance = float(total_balance)
        except (TypeError, ValueError):
            logger.warning("[Pipeline] Invalid total_balance, defaulting to free_cash + locked")
            total_balance = free_cash + locked_value

        # Guard against negative values
        if free_cash < 0:
            logger.warning("[Pipeline] Negative free_cash detected, setting to 0")
            free_cash = 0.0

        if locked_value < 0:
            logger.warning("[Pipeline] Negative locked_total detected, setting to 0")
            locked_value = 0.0

        if total_balance < 0:
            logger.warning("[Pipeline] Negative total_balance detected, recalculating")
            total_balance = free_cash + locked_value

        # Validate consistency: total_balance should be >= free_cash + locked_total
        expected_total = free_cash + locked_value
        if total_balance < expected_total:
            logger.warning(
                f"[Pipeline] Inconsistent wallet data: total_balance ({total_balance}) < free_cash + locked ({expected_total}), using calculated total"
            )
            total_balance = expected_total

        # Warn if zero cash (but allow it - agent will handle EMERGENCY mode)
        if free_cash == 0.0:
            logger.warning("[Pipeline] Zero free_cash detected - agent will trigger EMERGENCY mode")

        return {
            "free_cash": free_cash,
            "locked_total": locked_value,
            "total_balance": total_balance,
        }

    async def run_async(
        self,
        wallet_data: Optional[Dict[str, Any]] = None,
        transactions: Optional[List[Dict[str, Any]]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        start_time = time.time()

        try:
            wallet_data = self._validate_wallet(wallet_data)
            transactions = transactions or []
            user_context = user_context or {}

            # Run the LangGraph agent
            agent_result = await run_agent(
                wallet_data=wallet_data,
                transactions=transactions,
                user_context=user_context,
            )

            # Map agent_result keys to the shape copilot.run() expects:
            #   copilot expects: bayse, stress, bias, decision, allocation, wallet_data, student_model
            #   agent_result has: bayse, stress, bias, decision, allocation, student_model  ✓
            # The only mismatch is that pipeline.py previously called copilot with
            # the raw agent_result — but copilot.run() reads agent_result["allocation"]
            # and agent_result["decision"] which exist. Pass it directly.
            copilot_input = {
                "bayse":        agent_result.get("bayse", {}),
                "nlp":          agent_result.get("nlp", {}),
                "stress":       agent_result.get("stress", {}),
                "bias":         agent_result.get("bias", {}),
                "decision":     agent_result.get("decision", {}),
                "confidence":   agent_result.get("confidence", {}),
                "allocation":   agent_result.get("allocation", {}),
                "score":        agent_result.get("score", {}),
                "student_model":agent_result.get("student_model", {}),
                "wallet_data":  wallet_data,   # pass enriched wallet for survival signals
            }

            # Generate explanation using copilot
            explanation = await self.copilot.run(copilot_input)
            explanation = _to_dict(explanation)

            latency = round(time.time() - start_time, 3)

            # Return response in the same format as before for backward compatibility
            return {
                "meta": {
                    "latency_sec": latency,
                    "status": "success",
                },
                "student_model": agent_result.get("student_model", {}),
                "bayse": agent_result.get("bayse", {}),
                "nlp": agent_result.get("nlp", {}),
                "stress": agent_result.get("stress", {}),
                "bias": agent_result.get("bias", {}),
                "decision": agent_result.get("decision", {}),
                "confidence": agent_result.get("confidence", {}),
                "allocation": agent_result.get("allocation", {}),
                "score": agent_result.get("score", {}),
                "explanation": explanation,
                # Tool outputs
                "hustle_recommendations": agent_result.get("hustle_recommendations"),
                "purchase_safety_check": agent_result.get("purchase_safety_check"),
            }

        except Exception as exc:
            logger.exception("Pipeline failed: %s", exc)
            return {
                "meta": {
                    "status": "error",
                    "error": str(exc),
                }
            }

    def run(
        self,
        wallet_data: Optional[Dict[str, Any]] = None,
        transactions: Optional[List[Dict[str, Any]]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Synchronous wrapper for environments that are not already running an event loop.
        If you're already inside async code, call `await run_async(...)` instead.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            raise RuntimeError(
                "run() cannot be used inside an active event loop. "
                "Use `await run_async(...)` instead."
            )

        return asyncio.run(self.run_async(wallet_data, transactions, user_context))