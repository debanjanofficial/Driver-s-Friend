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
    
    async def process_message(self, message: str, language: str):
        # Extract keywords from user query
        keywords = self.processor.extract_keywords(message)

        # Search for matching regulations in the database
        results = self.db_ops.search_regulations(keywords, language)

        # If results are found, return the first match
        if results:
            return {
                "response": results[0]["content"],
                "intent": results[0]["category"],
                "confidence": 0.9  # Mock confidence score for simplicity
            }

        # Fallback response if no matches are found
        return {
            "response": f"I don't have information on '{message}' right now.",
            "intent": "unknown",
            "confidence": 0.5
        }
