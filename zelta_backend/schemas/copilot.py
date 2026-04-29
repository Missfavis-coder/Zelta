from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field

class CopilotMessage(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None

class CopilotRequest(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    question: str = Field(..., min_length=1)
    conversation_history: List[CopilotMessage] = Field(default_factory=list)

class ContextPill(BaseModel):
    # Added from_attributes here to stop the nested validation error
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    label: str
    value: str

class CopilotResponse(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    answer: str
    verdict: str = "HOLD"
    verdict_amount: float = 0.0
    context_pills: List[ContextPill] = Field(default_factory=list)
    confidence: float = 0.0
    sources: List[str] = Field(default_factory=list)

class CopilotAPIResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    success: bool
    data: CopilotResponse
