from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field

class CopilotMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None

class CopilotRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    question: str = Field(..., min_length=1)
    conversation_history: List[CopilotMessage] = Field(default_factory=list)

class ContextPill(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str
    value: str

class CopilotResponse(BaseModel):
    # from_attributes allows the model to interface with object instances
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
