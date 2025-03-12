from app.database.operations import DatabaseOperations
from app.nlp.processor import LanguageProcessor
from app.services.search_service import SearchService
from typing import List, Optional, Dict, Any

class ChatService:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        self.processor = LanguageProcessor()
        self.search_service = SearchService()

    async def process_message(self, message: str, language: str, user_id: Optional[str] = None):
        
        if user_id:
            await self._store_message(user_id, message, "user")
        # 1. First attempt to classify the intent
        processed_text = self.processor.process_text(message, language.split('-')[0])
        
        # Check if the message looks like a search query
        is_search_query = self._is_search_query(message)
        
        result = {}
        
        if is_search_query:
            # Handle as a search query
            search_results = await self.search_service.search_regulations(
                query=message,
                language=language,
                limit=3  # Limit to top 3 results for chat interface
            )
            
            if search_results["total_results"] > 0:
                # Format search results for chat
                response = self._format_search_results(search_results)
                return {
                    "response": response,
                    "intent": "search",
                    "confidence": 0.9,
                    "search_results": search_results["results"]
                }
                
                # Generate follow-up questions based on search results
                result["suggestions"] = self._generate_follow_up_questions(search_results)
                
                # Store response in history if user_id is provided
                if user_id:
                    await self._store_message(user_id, response, "bot", 
                                            search_results=search_results["results"])
                
                return result
        
        # 2. If not a search or no search results, fall back to regular processing
        keywords = self.processor.extract_keywords(message)
        results = self.db_ops.search_regulations(keywords, language)

        if results:
            response = results[0]["content"]
            intent = results[0].get("category", "unknown")
            result ={
                "response": response,
                "intent": intent,
                "confidence": 0.9,
                "suggestions": self._generate_related_questions(intent, language)
            }
        else:
            response = f"I don't have information on '{message}' right now. Try asking about specific driving rules or regulations."
            result = {
                "response": response,
                "intent": "unknown",
                "confidence": 0.5
            }
            
        if user_id:
            await self._store_message(user_id, response, "bot")
            
        return result
    
    async def get_user_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get chat history for a specific user"""
        # This would retrieve from a database collection storing chat history
        # For now, we'll return a mock implementation
        return []
    
    async def generate_suggestions(self, message: str, language: str) -> List[str]:
        """Generate contextual follow-up questions"""
        # Process the message to determine intent
        processed_text = self.processor.process_text(message, language.split('-')[0])
        keywords = self.processor.extract_keywords(message)
        results = self.db_ops.search_regulations(keywords, language)
        
        if results and len(results) > 0:
            intent = results[0].get("category", "unknown")
            return self._generate_related_questions(intent, language)
        return []
    
    async def get_popular_questions(self, language: str, limit: int = 5) -> List[str]:
        """Get popular driving-related questions"""
        popular_questions = {
            "en-US": [
                "What is the speed limit on highways?",
                "Do I need to carry my driving license?",
                "What's the alcohol limit for drivers?",
                "When should I use headlights?",
                "How do traffic circles work?"
            ],
            "de": [
                "Wie hoch ist die Geschwindigkeitsbegrenzung auf Autobahnen?",
                "Muss ich meinen Führerschein mitführen?",
                "Wie hoch ist die Alkoholgrenze für Fahrer?",
                "Wann sollte ich die Scheinwerfer einschalten?",
                "Wie funktionieren Verkehrskreisel?"
            ]
        }
        
        lang_key = "en-US"
        if language.startswith("de"):
            lang_key = "de"
            
        questions = popular_questions.get(lang_key, popular_questions["en-US"])
        return questions[:limit]
    
    def _is_search_query(self, message: str) -> bool:
        """Determine if a message looks like a search query"""
        search_indicators = ["search", "find", "look up", "search for", "where", "how to", "information about"]
        message_lower = message.lower()
        
        # Check if message starts with or contains search indicators
        for indicator in search_indicators:
            if message_lower.startswith(indicator) or f" {indicator} " in message_lower:
                return True
                
        # Check if message has question format
        if message_lower.startswith(("what", "where", "how", "when", "which", "who", "why")):
            return True
            
        # If message is longer than 4 words, it's likely a search
        if len(message.split()) > 4:
            return True
            
        return False
    
    def _format_search_results(self, search_results):
        """Format search results into a readable chat response"""
        if search_results["total_results"] == 0:
            return "I couldn't find any information about that. Try asking a different question."
            
        response = "Here's what I found about your question:\n\n"
        
        for i, result in enumerate(search_results["results"], 1):
            response += f"{i}. {result['content']}\n"
            if result.get('source'):
                response += f"   Source: {result['source']}\n"
            response += "\n"
            
        return response.strip()
    
    def _generate_follow_up_questions(self, search_results) -> List[str]:
        """Generate follow-up questions based on search results"""
        if search_results["total_results"] == 0:
            return []
            
        questions = []
        for result in search_results["results"]:
            category = result.get("category")
            if category == "speed_limit":
                questions.append(f"What happens if I exceed the speed limit?")
                questions.append(f"Are there different speed limits at night?")
            elif category == "alcohol_limit":
                questions.append(f"What are the penalties for drunk driving?")
                questions.append(f"How long should I wait after drinking before driving?")
            
        return questions[:3]  # Return at most 3 suggestions
    
    def _generate_related_questions(self, intent: str, language: str) -> List[str]:
        """Generate related questions based on intent"""
        questions = {
            "speed_limit": {
                "en-US": [
                    "What's the speed limit on highways?",
                    "What happens if I exceed the speed limit?",
                    "Are there different speed limits for trucks?"
                ],
                "de": [
                    "Wie hoch ist die Geschwindigkeitsbegrenzung auf Autobahnen?",
                    "Was passiert, wenn ich die Geschwindigkeitsbegrenzung überschreite?",
                    "Gibt es unterschiedliche Geschwindigkeitsbegrenzungen für LKWs?"
                ]
            },
            "alcohol_limit": {
                "en-US": [
                    "What are the penalties for drunk driving?",
                    "Is the alcohol limit different for new drivers?",
                    "How long should I wait after drinking before driving?"
                ],
                "de": [
                    "Welche Strafen gibt es für Trunkenheit am Steuer?",
                    "Ist die Alkoholgrenze für Fahranfänger anders?",
                    "Wie lange sollte ich nach dem Trinken warten, bevor ich fahre?"
                ]
            }
        }
        
        lang_key = "en-US"
        if language.startswith("de"):
            lang_key = "de"
        
        return questions.get(intent, {}).get(lang_key, [])
    
    async def _store_message(self, user_id: str, content: str, sender: str, **kwargs):
        """Store a message in the user's chat history"""
        # In a real implementation, this would store the message in a database
        # Example implementation:
        # self.db_ops.insert_chat_message({
        #     "user_id": user_id,
        #     "content": content,
        #     "sender": sender,
        #     "timestamp": datetime.now(),
        #     **kwargs
        # })
        pass