"""
Behavioral routes.

GET /api/behavioral/snapshot
Returns a deep-dive explanation of the user's current behavior.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException

from core.dependencies import get_db, get_user_id
from schemas.behavioral import BehavioralSnapshotResponse
from services.behavioral_service import get_behavioral_snapshot

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/behavioral", tags=["Behavioral"])


@router.get("/snapshot", response_model=BehavioralSnapshotResponse)
async def behavioral_snapshot(
    db=Depends(get_db),
    uid: str = Depends(get_user_id),
):
    """
    Return the current behavioral snapshot for the authenticated user.
    """
    try:
        snapshot = await get_behavioral_snapshot(db, uid)
        return BehavioralSnapshotResponse(
            success=True,
            data=snapshot,
            uid=uid,
        )

    except Exception as exc:
        logger.exception("Behavioral snapshot failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail=f"Could not build behavioral snapshot: {str(exc)}",
        )
