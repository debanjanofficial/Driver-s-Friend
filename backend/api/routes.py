from fastapi import APIRouter, Depends
from .models import ChatRequest, ChatResponse
from ..nlp.processor import LanguageProcessor
from ..nlp.intent_classifier import IntentClassifier
from ..nlp.response_generator import ResponseGenerator
from ..database.operations import DatabaseOperations

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Process the incoming message
    nlp_processor = LanguageProcessor()
    processed_text = nlp_processor.process_text(request.message, request.language)
    
    # Classify intent
    intent_classifier = IntentClassifier()
    intent = intent_classifier.predict(processed_text)
    
    # Generate response
    db_ops = DatabaseOperations()
    response_gen = ResponseGenerator(db_ops)
    response = response_gen.generate_response(intent, request.language)
    
    return ChatResponse(
        response=response,
        intent=intent.name,
        confidence=intent.confidence
    )

@router.get("/regulations/{category}")
async def get_regulations(category: str, language: str):
    db_ops = DatabaseOperations()
    regulations = db_ops.get_regulations(category, language)
    return regulations
