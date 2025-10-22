from fastapi import APIRouter, Query
from app.services.search_service import SearchService
from app.api.models import ChatRequest, ChatResponse, SearchRequest, SearchResult, SearchResponse
from app.services.chat_service import ChatService
from app.database.operations import DatabaseOperations
from typing import List, Optional

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    chat_service = ChatService()
    result = await chat_service.process_message(
        message=request.message,
        language=request.language,
        user_id=request.user_id
    )
    return ChatResponse(
        response=result["response"],
        intent=result["intent"],
        confidence=result["confidence"],
        search_results= result.get("search_results"),
        suggestions=result.get("suggestions"),
        source=result.get("source"),
        url=result.get("url")
    )
    
@router.get("/chat/history/{user_id}")
async def get_chat_history(user_id: str, limit: int = 10):
    chat_service = ChatService()
    history = await chat_service.get_user_history(user_id, limit)
    return {"history": history}

@router.post("/chat/suggestions")
async def get_suggestions(request: ChatRequest):
    chat_service = ChatService()
    suggestions = await chat_service.generate_suggestions(
        message=request.message,
        language=request.language
    )
    return {"suggestions": suggestions}
    
@router.post("/search", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest):
    search_service = SearchService()
    result = await search_service.search_regulations(
        query=request.query,
        language=request.language,
        category=request.category,
        limit=request.limit
    )
    return result

@router.get("/categories")
async def get_categories(language: str = Query("en-US")):
    db_ops = DatabaseOperations()
    categories = db_ops.get_categories(language)
    return {"categories": categories}

@router.get("/popular-questions")
async def get_popular_questions(language: str = Query("en-US"), limit: int = 5):
    chat_service = ChatService()
    questions = await chat_service.get_popular_questions(language, limit)
    return {"questions": questions}

@router.get("/health")
async def health_check():
    return {"status": "OK"}
