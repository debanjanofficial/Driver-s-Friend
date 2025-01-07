from fastapi import APIRouter, HTTPException
from app.api.models import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

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
        confidence=result["confidence"]
    )

@router.get("/health")
async def health_check():
    return {"status": "OK"}
