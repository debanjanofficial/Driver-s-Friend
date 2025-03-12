from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    language: str

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    
class SearchRequest(BaseModel):
    query: str
    language: str
    category: Optional[str] = None
    limit: Optional[int] = 10
    
class SearchResult(BaseModel):
    category: str
    content: str
    country: str
    source: str
    
class SearchResponse(BaseModel):
    results: List[dict]
    query: str
    matched_keywords: List[str]
    total_results: int
