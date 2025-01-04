from ..nlp.processor import LanguageProcessor
from ..nlp.intent_classifier import IntentClassifier
from ..nlp.response_generator import ResponseGenerator
from ..database.operations import DatabaseOperations

class ChatService:
    def __init__(self):
        self.nlp_processor = LanguageProcessor()
        self.intent_classifier = IntentClassifier()
        self.db_ops = DatabaseOperations()
        self.response_generator = ResponseGenerator(self.db_ops)
    
    async def process_message(self, message: str, language: str, 
                            user_id: Optional[str] = None):
        # Process message
        processed_text = self.nlp_processor.process_text(message, language)
        
        # Get intent
        intent = self.intent_classifier.predict(processed_text)
        
        # Generate response
        response = self.response_generator.generate_response(
            intent.name, language
        )
        
        # Log interaction
        if user_id:
            self.db_ops.log_chat_interaction(
                user_id, message, intent.name, response
            )
        
        return {
            "response": response,
            "intent": intent.name,
            "confidence": intent.confidence
        }
