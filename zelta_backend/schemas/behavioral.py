"""
Behavioral Snapshot schemas.

This feature explains why ZELTA flagged the user's current behavior
as irrational, using live brain output + recent wallet evidence.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BehavioralEvidence(BaseModel):
    transaction: str
    date: str
    trigger: str
    bayse_fear_at_time: float
    zelta_model_at_time: float
    gap: float
    plain_english: str


class InstinctSay(BaseModel):
    action: str
    amount: float


class MathSay(BaseModel):
    action: str
    amount: float


class BayseContext(BaseModel):
    crowd_fear: float
    zelta_model: float
    gap: float
    market_title: str = ""


class BehavioralSnapshot(BaseModel):
    active_bias: str
    confidence: str
    explanation: str

    evidence: List[BehavioralEvidence] = Field(default_factory=list)

    instinct_says: InstinctSay
    math_says: MathSay

    correction_value: float
    correction_plain: str

    bayse_context: BayseContext


class BehavioralSnapshotResponse(BaseModel):
    success: bool = True
    data: BehavioralSnapshot
    uid: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class BehavioralSnapshotSummary(BaseModel):
    active_bias: str
    confidence: str
    explanation: str
    correction_value: float
    correction_plain: str
    bayse_context: BayseContext
