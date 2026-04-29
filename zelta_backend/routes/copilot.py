import asyncio
import logging
from fastapi import APIRouter, HTTPException, status

from core.dependencies import CurrentUser, DB
from services.copilot_service import answer_question
from services.intelligence_service import get_intelligence
from services.wallet_service import get_wallet_summary
from schemas.copilot import CopilotRequest, CopilotAPIResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/copilot", tags=["BQ Co-Pilot"])

@router.post("", response_model=CopilotAPIResponse)
async def ask_copilot(
    current_user: CurrentUser,
    db: DB,
    request: CopilotRequest,
):
    uid = current_user["uid"]

    # 1. Load context concurrently to reduce latency
    # We use return_exceptions=True so one failure doesn't kill the other
    tasks = [get_intelligence(db, uid), get_wallet_summary(db, uid)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 2. Extract Brain Context
    if isinstance(results[0], Exception):
        logger.warning("Brain context load failed for uid=%s: %s", uid, results[0])
        brain_context = {}
    else:
        brain_context = results[0].model_dump()

    # 3. Extract Wallet Context
    if isinstance(results[1], Exception):
        logger.warning("Wallet context load failed for uid=%s: %s", uid, results[1])
        wallet_context = {}
    else:
        wallet_context = results[1].model_dump()

    try:
        # 4. Orchestrate the answer
        response = await answer_question(
            db=db,
            uid=uid,
            request=request,
            brain_context=brain_context,
            wallet_context=wallet_context,
        )

        return CopilotAPIResponse(success=True, data=response)

    except Exception as e:
        logger.error("Critical Copilot failure for %s: %s", uid, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The Co-Pilot is having trouble processing that right now. Please try again shortly.",
        )
