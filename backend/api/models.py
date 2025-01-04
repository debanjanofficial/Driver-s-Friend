from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    language: str
    user_id: Optional[str]

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
