from app.nlp.processor import LanguageProcessor
from app.nlp.intent_classifier import IntentClassifier
from app.nlp.response_generator import ResponseGenerator
from app.database.operations import DatabaseOperations

class ChatService:
    def __init__(self):
        self.nlp_processor = LanguageProcessor()
        self.intent_classifier = IntentClassifier()
        self.db_ops = DatabaseOperations()
        self.response_generator = ResponseGenerator(self.db_ops)
    
    async def process_message(self, message: str, language: str, user_id: str = None):
        processed_text = self.nlp_processor.process_text(message, language)
        intent = self.intent_classifier.predict(processed_text)
        
        response = self.response_generator.generate_response(
            intent.name,language)
        
        # Log chat if user_id is provided
        if user_id:
            self.db_ops.log_chat_interaction(user_id, message, intent.name, response)
        
        return {
            "response": response,
            "intent": intent.name,
            "confidence": intent.confidence
        }
