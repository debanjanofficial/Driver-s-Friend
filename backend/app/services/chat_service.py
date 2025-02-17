from backend.app.database.operations import DatabaseOperations
from backend.app.nlp.processor import LanguageProcessor

class ChatService:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        self.processor = LanguageProcessor()

    async def process_message(self, message: str, language: str):
        # 1. Tokenize user query to extract keywords
        keywords = self.processor.extract_keywords(message)

        # 2. Search the database for matching regulations
        results = self.db_ops.search_regulations(keywords, language)

        # 3. Return the first found record or a fallback
        if results:
            return {
                "response": results[0]["content"],
                "intent": results[0].get("category", "unknown"),
                "confidence": 0.9
            }
        else:
            return {
                "response": f"I don't have information on '{message}' right now.",
                "intent": "unknown",
                "confidence": 0.5
            }
