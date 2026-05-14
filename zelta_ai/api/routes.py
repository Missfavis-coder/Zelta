import time
import uuid
import logging
import asyncio
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from security import verify_internal_request
from brain.pipeline import ZeltaPipeline
from brain.bayse.stress_signal import monitor
from brain.copilot.gemini import ZeltaCopilot


logger = logging.getLogger("zelta.api")

# Versioned router (future-proof)
router = APIRouter(prefix="/brain/v1", tags=["AI Brain"])
public_router = APIRouter(tags=["Public API"])

pipeline = ZeltaPipeline()

# Lazy-loaded Copilot (prevents crash if env not ready)
_copilot: Optional[ZeltaCopilot] = None


def get_copilot() -> ZeltaCopilot:
    global _copilot
    if _copilot is None:
        _copilot = ZeltaCopilot()
    return _copilot


# =========================
# REQUEST MODELS
# =========================

class WalletData(BaseModel):
    free_cash: float = Field(default=26500.0, ge=0)
    locked_total: float = Field(default=18500.0, ge=0)
    total_balance: float = Field(default=45000.0, ge=0)


class Transaction(BaseModel):
    amount: float
    category: str
    type: str
    description: Optional[str] = None


class BrainRequest(BaseModel):
    wallet_data: WalletData = Field(default_factory=WalletData)
    transactions: List[Transaction] = Field(default_factory=list)
    user_context: Dict[str, Any] = Field(default_factory=dict)


class CopilotQuestionRequest(BaseModel):
    question: str = Field(..., min_length=3)
    context: Dict[str, Any] = Field(default_factory=dict)


# =========================
# HELPERS
# =========================

def _safe_event_title(event: Dict[str, Any]) -> str:
    return event.get("title") or event.get("name") or event.get("description") or "Unknown"


def _safe_market_id(market: Dict[str, Any]) -> Optional[str]:
    return market.get("id") or market.get("marketId") or market.get("market_id")


def _extract_events(raw: Any) -> List[Dict[str, Any]]:
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]

    if not isinstance(raw, dict):
        return []

    candidates = (
        raw.get("data"),
        raw.get("events"),
        raw.get("items"),
        raw.get("results"),
    )

    for candidate in candidates:
        if isinstance(candidate, list):
            return [item for item in candidate if isinstance(item, dict)]
        if isinstance(candidate, dict):
            nested = candidate.get("events") or candidate.get("items") or candidate.get("results")
            if isinstance(nested, list):
                return [item for item in nested if isinstance(item, dict)]

    return []


# =========================
# CORE ENDPOINTS
# =========================

@router.get("/health")
def health():
    signal = monitor.get_signal() or {}

    return {
        "status": "ok",
        "service": "ZELTA AI Brain",
        "bayse_connected": True,
        "current_stress": signal.get("score", 50),
        "stress_level": signal.get("status", "UNKNOWN"),
        "mode": "stateless",
        "version": "1.0.0",
    }


@router.post("/intelligence")
async def get_intelligence(
    request: BrainRequest,
    _: None = Depends(verify_internal_request),
):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        wallet_dict = request.wallet_data.model_dump()
        transactions = [t.model_dump() for t in request.transactions]
        user_context = request.user_context or {}

        enriched_wallet = {
            **wallet_dict,
            "transaction_count": len(transactions),
            "has_expenses": any(str(t.get("type", "")).lower() in {"expense", "debit"} for t in transactions),
            "has_income": any(str(t.get("type", "")).lower() in {"income", "credit"} for t in transactions),
            "user_flags": user_context.get("flags", []),
        }

        result = await pipeline.run_async(
            wallet_data=enriched_wallet,
            transactions=transactions,
            user_context=user_context,
        )

        if result.get("meta", {}).get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail=result["meta"].get("error", "Brain processing failed"),
            )

        latency = round(time.time() - start_time, 3)

        return {
            "success": True,
            "request_id": request_id,
            "latency_sec": latency,
            "data": result,
            "meta": {
                "status": "success",
                "brain_latency_sec": latency,
                "request_id": request_id,
            },
        }

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception("get_intelligence failed: %s", exc)
        latency = round(time.time() - start_time, 3)

        return {
            "success": False,
            "request_id": request_id,
            "latency_sec": latency,
            "error": str(exc),
            "meta": {"status": "error"},
            "data": {
                "allocation": {"verdict": "HOLD"},
                "confidence": {"is_actionable": False},
                "stress": {"score": 50, "level": "UNKNOWN"},
                "bias": {"bias": "Unknown"},
            },
        }


# =========================
# COPILOT ENDPOINT
# =========================

@router.post("/ask")
async def ask_copilot(
    request: CopilotQuestionRequest,
    _: None = Depends(verify_internal_request),
):
    try:
        answer = await asyncio.wait_for(
            get_copilot().answer_question(
                question=request.question,
                context=request.context,
            ),
            timeout=10,
        )

        return {
            "success": True,
            "data": {
                "answer": answer,
            },
        }

    except asyncio.TimeoutError:
        logger.warning("Copilot timeout | question=%s", request.question)
        return {
            "success": False,
            "data": {"answer": "Response taking too long. Try again."},
        }

    except Exception as e:
        logger.exception("Copilot ask failed | question=%s | error=%s", request.question, e)
        return {
            "success": False,
            "data": {"answer": "Unable to answer right now. Try again later."},
        }


from brain.tools.hustle_templates import get_hustle_templates, HUSTLE_CATALOG


# =========================
# HUSTLE TEMPLATES ENDPOINT
# =========================

class HustleTemplateRequest(BaseModel):
    agent_mode: str = Field(default="NORMAL", description="EMERGENCY | SURVIVAL | NORMAL")
    free_cash:  float = Field(default=0.0, ge=0)


@router.get("/hustle-templates")
async def get_hustle_templates_endpoint(
    agent_mode: str = "NORMAL",
    free_cash: float = 0.0,
    _: None = Depends(verify_internal_request),
):
    """
    Fix 8: Returns campus hustle templates filtered by the student's
    current agent mode and available free cash.

    Query params:
      - agent_mode: EMERGENCY | SURVIVAL | NORMAL  (default: NORMAL)
      - free_cash:  student's current free cash in NGN (default: 0)
    """
    try:
        student_model = {
            "agent_mode": agent_mode.upper(),
            "free_cash":  free_cash,
        }
        result = get_hustle_templates.invoke({"student_model": student_model})
        return {
            "success": True,
            "agent_mode": agent_mode.upper(),
            "free_cash": free_cash,
            "count": len(HUSTLE_CATALOG),
            "recommendations": result,
        }
    except Exception as exc:
        logger.exception("get_hustle_templates_endpoint failed: %s", exc)
        return {
            "success": False,
            "error": str(exc),
            "recommendations": "",
        }


@router.post("/hustle-templates")
async def post_hustle_templates_endpoint(
    request: HustleTemplateRequest,
    _: None = Depends(verify_internal_request),
):
    """POST variant — accepts body instead of query params."""
    return await get_hustle_templates_endpoint(
        agent_mode=request.agent_mode,
        free_cash=request.free_cash,
    )

@public_router.get("/api/stress")
async def get_stress():
    signal = monitor.get_signal() or {}

    return {
        "score": signal.get("score", 50),
        "status": signal.get("status", "UNKNOWN"),
        "market_title": signal.get("market_title"),
        "market_id": signal.get("market_id"),
        "mid_price": signal.get("mid_price"),
        "spread": signal.get("spread"),
        "volume24h": signal.get("volume24h"),
        "updated_at": signal.get("updated_at"),
        "source": "Bayse Prediction Markets",
    }


@public_router.get("/api/markets")
async def get_markets():
    try:
        events_resp = await monitor.client.get_events()
        events = _extract_events(events_resp)

        markets = []
        for event in events[:25]:
            for market in event.get("markets", []):
                market_id = _safe_market_id(market)
                if not market_id:
                    continue

                markets.append(
                    {
                        "event_title": _safe_event_title(event),
                        "market_id": market_id,
                        "market_title": market.get("title") or market.get("name") or "Unknown",
                    }
                )

        return {
            "count": len(markets),
            "markets": markets,
        }

    except Exception as exc:
        logger.exception("get_markets failed: %s", exc)
        return {
            "count": 0,
            "markets": [],
            "error": str(exc),
        }