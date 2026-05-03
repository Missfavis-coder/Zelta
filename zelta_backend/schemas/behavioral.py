"""
Behavioral Snapshot + Behavioral Pattern schemas.

Behavioral Snapshot:
Explains why ZELTA flagged the user's current behavior as irrational.

Behavioral Pattern:
Shows the user's 8-week behavioral trend across time.
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


class DecisionConfidence(BaseModel):
    rational_pct: float
    behavioral_pct: float
    gap: float
    confidence_score: float = 0.0
    confidence_tier: str = "Low"
    intervention_urgency: str = "MODERATE"
    plain_english: str = ""


class BehavioralBiasCard(BaseModel):
    bias: str
    status: str
    current_strength: float
    explanation: str


class BehavioralSnapshot(BaseModel):
    active_bias: str
    confidence: str
    explanation: str

    bayse_context: BayseContext
    decision_confidence: DecisionConfidence

    bias_strength_label: str = "LOW"
    bias_strength_value: float = 0.0

    evidence: List[BehavioralEvidence] = Field(default_factory=list)
    tracked_biases: List[BehavioralBiasCard] = Field(default_factory=list)

    instinct_says: InstinctSay
    math_says: MathSay

    correction_value: float
    correction_plain: str

    recommendation: str = ""


class BehavioralSnapshotResponse(BaseModel):
    success: bool = True
    data: BehavioralSnapshot
    uid: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class BehavioralWeekItem(BaseModel):
    week: str
    bias: str
    strength: float
    note: str = ""
    confidence_label: str = "LOW"


class BehavioralPattern(BaseModel):
    weeks: List[BehavioralWeekItem] = Field(default_factory=list)
    dominant_bias: str = "None"
    summary: str = ""
    recommendation: str = ""
    confidence_gap: float = 0.0


class BehavioralPatternResponse(BaseModel):
    success: bool = True
    data: BehavioralPattern
    uid: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)
