from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    language: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    search_results: Optional[List[dict]] = None
    suggestions: Optional[List[str]] = None
    source: Optional[str] = None
    url: Optional[str] = None
    
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
