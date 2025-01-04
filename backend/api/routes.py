# backend/api/routes.py
from fastapi import APIRouter, HTTPException
from .models import ChatRequest, ChatResponse
from ..nlp.processor import LanguageProcessor
from ..nlp.intent_classifier import IntentClassifier
from ..nlp.response_generator import ResponseGenerator
from ..database.operations import DatabaseOperations

router = APIRouter()
nlp_processor = LanguageProcessor()
intent_classifier = IntentClassifier()
db_ops = DatabaseOperations()
response_generator = ResponseGenerator(db_ops)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Process the incoming message
        processed_text = nlp_processor.process_text(
            request.message, 
            request.language
        )
        
        # Classify intent
        intent = intent_classifier.predict(processed_text)
        
        # Generate response
        response = response_generator.generate_response(
            intent, 
            request.language
        )
        
        return ChatResponse(
            response=response,
            intent=intent,
            confidence=0.85  # Replace with actual confidence score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/regulations/{category}")
async def get_regulations(category: str, language: str):
    try:
        regulations = db_ops.get_regulation(category, language)
        if not regulations:
            raise HTTPException(status_code=404, detail="Regulation not found")
        return regulations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
