"""
Behavioral routes.

GET /api/behavioral/snapshot
Returns a deep-dive explanation of the user's current behavior.

GET /api/behavioral/pattern
Returns the 8-week behavioral pattern.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException

from core.dependencies import DB, CurrentUser
from schemas.behavioral import (
    BehavioralPatternResponse,
    BehavioralSnapshotResponse,
)
from services.behavioral_service import (
    get_behavioral_pattern,
    get_behavioral_snapshot,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/behavioral", tags=["Behavioral"])


@router.get("/snapshot", response_model=BehavioralSnapshotResponse)
async def behavioral_snapshot(
    db: DB,
    current_user: CurrentUser,
):
    try:
        uid = current_user["uid"]

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


@router.get("/pattern", response_model=BehavioralPatternResponse)
async def behavioral_pattern(
    db: DB,
    current_user: CurrentUser,
):
    """
    Return the 8-week behavioral pattern for the authenticated user.
    """
    try:
        uid = current_user["uid"]
        pattern = await get_behavioral_pattern(db, uid)
        return BehavioralPatternResponse(
            success=True,
            data=pattern,
            uid=uid,
        )

    except Exception as exc:
        logger.exception("Behavioral pattern failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail=f"Could not build behavioral pattern: {str(exc)}",
        )
