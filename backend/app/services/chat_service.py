from app.database.operations import DatabaseOperations
from app.nlp.processor import LanguageProcessor
from app.services.search_service import SearchService
from app.services.web_scraper import WebSearchService
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatService:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        self.processor = LanguageProcessor()
        self.search_service = SearchService()
        self.web_search_service = WebSearchService()
        # Conversation memory storage - in production, this should be persisted in a database
        self.conversation_memory: Dict[str, List[Dict[str, Any]]] = {}

    async def process_message(self, message: str, language: str, user_id: Optional[str] = None):
        
        # Add conversation memory
        if user_id:
            await self._store_message(user_id, message, "user")
            # Get conversation context for contextual responses
            conversation_context = self._get_conversation_context(user_id)
        else:
            conversation_context = []
            
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
        
        # 2. If not a search query or no search results, prioritize web search for comprehensive answers
        # Try web search first for the most up-to-date information
        web_response = self.web_search_service.search_route_to_germany(message, language)
        
        if web_response:
            result = web_response
            # Format the response to clearly indicate it's from the web
            if language.startswith("de"):
                response = f"Laut {result['source']}:\n\n{result['response']}\n\nQuelle: {result['url']}"
            else:
                response = f"According to {result['source']}:\n\n{result['response']}\n\nSource: {result['url']}"
            result["response"] = response
        else:
            # Fallback to database if web search fails
            keywords = self.processor.extract_keywords(message)
            try:
                results = self.db_ops.search_regulations(keywords, language)
            except:
                results = []  # Database unavailable, use offline knowledge
            
            if results:
                response = results[0]["content"]
                intent = results[0].get("category", "unknown")
                result = {
                    "response": response,
                    "intent": intent,
                    "confidence": 0.8,  # Lower confidence for database vs web
                    "suggestions": self._generate_related_questions(intent, language)
                }
            else:
                # Final fallback to offline knowledge base
                offline_response = self._get_offline_response(message, language)
                if offline_response:
                    result = offline_response
                    # Add note that this is from offline knowledge
                    if language.startswith("de"):
                        result["response"] = f"[Offline-Wissensdatenbank] {result['response']}"
                    else:
                        result["response"] = f"[Offline Knowledge Base] {result['response']}"
                    response = result["response"]
                else:
                    # No information found anywhere
                    if language.startswith("de"):
                        response = f"Ich konnte leider keine Informationen zu '{message}' finden. Versuchen Sie, Ihre Frage anders zu formulieren oder nach spezifischen Verkehrsregeln zu fragen."
                    else:
                        response = f"I couldn't find any information about '{message}'. Try rephrasing your question or asking about specific driving rules."
                    result = {
                        "response": response,
                        "intent": "unknown",
                        "confidence": 0.3
                    }
            
        if user_id:
            # Add contextual elements to the response
            if "response" in result:
                result["response"] = self._add_contextual_elements(
                    result["response"], 
                    conversation_context, 
                    language
                )
            await self._store_message(user_id, result.get("response", ""), "assistant")
            
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
            # Always show "Our Database" as source for database results
            response += f"   Source: Our Database\n"
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
    
    def _get_offline_response(self, message: str, language: str) -> Optional[Dict[str, Any]]:
        """Provide responses using offline knowledge base when database is unavailable"""
        message_lower = message.lower()
        
        # Define offline knowledge base
        offline_knowledge = {
            "en-US": {
                "speed_limit": {
                    "keywords": ["speed", "limit", "fast", "mph", "kmh", "highway", "city", "urban"],
                    "response": "Speed limits vary by location and road type. Generally:\n• City/Urban areas: 25-35 mph (40-55 km/h)\n• Suburban areas: 35-45 mph (55-70 km/h)\n• Highways: 55-80 mph (90-130 km/h)\n• School zones: 15-25 mph (25-40 km/h)\n\nAlways check local speed limit signs as they may differ.",
                    "intent": "speed_limit"
                },
                "phone_driving": {
                    "keywords": ["phone", "cell", "mobile", "text", "call", "hands-free"],
                    "response": "Using a phone while driving is restricted in most places:\n• Handheld devices are typically prohibited\n• Hands-free calling is usually allowed\n• Texting while driving is illegal in most jurisdictions\n• Use voice commands or pull over safely to use your phone\n• Always prioritize safety over convenience.",
                    "intent": "phone_usage"
                },
                "alcohol_limit": {
                    "keywords": ["alcohol", "drink", "blood", "bac", "drunk", "dui", "dwi", "limit"],
                    "response": "Blood Alcohol Content (BAC) limits for drivers:\n• Most countries: 0.08% (0.08 g/100ml)\n• Some countries (like Germany): 0.05%\n• Commercial drivers: Often 0.04% or lower\n• New/young drivers: May have 0.00% tolerance\n\nBest practice: Don't drink and drive at all. Use designated drivers, taxis, or public transport.",
                    "intent": "alcohol_limit"
                },
                "seatbelt": {
                    "keywords": ["seatbelt", "seat belt", "buckle", "safety belt", "safety requirement", "safety", "belt"],
                    "response": "Seatbelt safety requirements:\n• Driver and all passengers must wear seatbelts\n• Children require appropriate car seats/booster seats based on age/weight\n• Front and rear seat passengers are required to buckle up\n• Failure to wear seatbelts can result in fines\n• Seatbelts reduce injury risk by about 45% and death risk by 50%\n• Always adjust seatbelt properly across chest and hips",
                    "intent": "safety_requirements"
                },
                "child_safety": {
                    "keywords": ["child seat", "car seat", "booster", "children", "kids", "infant", "toddler"],
                    "response": "Child safety seat requirements:\n• Rear-facing seats: Birth to 2 years (or until max height/weight)\n• Forward-facing seats: 2-4 years with harness\n• Booster seats: 4-8 years (until seatbelt fits properly)\n• Children under 13 should ride in back seat\n• Always follow manufacturer's instructions\n• Replace car seats after accidents",
                    "intent": "safety_requirements"
                },
                "phone_usage": {
                    "keywords": ["phone", "cell", "mobile", "text", "call", "hands-free", "bluetooth", "driving", "safety requirement"],
                    "response": "Phone usage safety requirements while driving:\n• Handheld phone calls are prohibited in most places\n• Texting while driving is illegal and extremely dangerous\n• Use hands-free/Bluetooth devices for calls\n• Voice commands are safer than manual input\n• Pull over safely if you must use your phone\n• Never text, email, or browse while driving",
                    "intent": "safety_requirements"
                },
                "stop_sign": {
                    "keywords": ["stop", "sign", "intersection", "complete stop"],
                    "response": "At a stop sign:\n• Come to a complete stop before the stop line\n• If no stop line, stop before entering the crosswalk\n• If no crosswalk, stop before entering the intersection\n• Look left, right, then left again\n• Yield to pedestrians and other vehicles with right-of-way\n• Proceed only when safe",
                    "intent": "stop_sign"
                },
                "parking": {
                    "keywords": ["park", "parking", "parallel", "reverse", "space", "curb", "meter", "zone"],
                    "response": "Parking regulations and tips:\n• No parking within 15 feet of fire hydrants\n• No parking in handicapped spaces without permits\n• Check time limits and pay parking meters\n• Parallel parking: Find space 1.5x car length, align mirrors, reverse with full turn, straighten, adjust\n• Don't block driveways, crosswalks, or bus stops\n• Park in same direction as traffic flow",
                    "intent": "parking_regulations"
                },
                "right_of_way": {
                    "keywords": ["right", "way", "yield", "priority", "who goes first", "intersection", "stop sign", "traffic light"],
                    "response": "Right-of-way rules at intersections:\n• At 4-way stop: First to arrive goes first, if simultaneous arrival, rightmost vehicle goes\n• At uncontrolled intersection: Vehicle on right has right-of-way\n• Left turns always yield to oncoming traffic\n• Emergency vehicles (ambulance, fire, police) always have right-of-way\n• Pedestrians have right-of-way at marked crosswalks\n• When in doubt, yield and proceed cautiously",
                    "intent": "right_of_way"
                },
                "traffic_signs": {
                    "keywords": ["traffic signs", "stop sign", "yield", "speed limit sign", "warning", "regulatory", "guide signs"],
                    "response": "Common traffic signs and meanings:\n• STOP: Complete stop required before proceeding\n• YIELD: Slow down, give right-of-way to other traffic\n• Speed Limit: Maximum safe speed allowed\n• No Parking: Parking prohibited in this area\n• School Zone: Reduced speed when children present\n• Construction Zone: Slow down, workers present\n• Always obey all posted traffic signs",
                    "intent": "traffic_signs"
                },
                "greeting": {
                    "keywords": ["hello", "hi", "help", "what can you do", "how are you", "hey", "good morning", "good afternoon", "good evening", "hey there", "what can you help", "what do you do"],
                    "response": "Hello! I'm Driver's Friend, your driving regulations assistant. I can help you with:\n• Speed limits and traffic rules\n• Parking regulations\n• Right-of-way rules\n• Safety requirements (seatbelts, phone usage)\n• Alcohol limits and DUI laws\n• Traffic signs and signals\n\nWhat driving question can I help you with today?",
                    "intent": "greeting"
                },
                "farewell": {
                    "keywords": ["bye", "goodbye", "see you", "thanks", "thank you", "thx", "that's all", "nothing else", 
                               "thanks for your help", "thank you for your help", "appreciate it", "thank you so much", 
                               "thanks a lot", "many thanks", "i appreciate it", "appreciate your help", "helpful", 
                               "you helped me", "this helped", "very helpful"],
                    "response": "You're welcome! Drive safely and feel free to ask me anytime about traffic rules. Have a great day! 🚗",
                    "intent": "farewell"
                },
                "help": {
                    "keywords": ["help me", "what can you do", "capabilities", "features", "what do you know", "how can you help"],
                    "response": "I'm your personal driving assistant! I can help you with:\n\n🚦 Traffic Rules & Regulations\n🚗 Speed limits for different areas\n📱 Phone usage while driving\n🍺 Alcohol limits and DUI laws\n🔧 Parking and maneuvering tips\n⚠️ Safety requirements and best practices\n\nJust ask me any driving-related question!",
                    "intent": "help"
                }
            },
            "de": {
                "speed_limit": {
                    "keywords": ["geschwindigkeit", "limit", "schnell", "kmh", "autobahn", "stadt"],
                    "response": "Geschwindigkeitsbegrenzungen in Deutschland:\n• Innerorts: 50 km/h\n• Außerorts: 100 km/h\n• Autobahn: Richtgeschwindigkeit 130 km/h (oft keine Begrenzung)\n• Spielstraße: Schrittgeschwindigkeit\n• Bei Regen/schlechten Bedingungen gelten niedrigere Limits",
                    "intent": "speed_limit"
                },
                "alcohol_limit": {
                    "keywords": ["alkohol", "promille", "trinken", "betrunken", "fahren"],
                    "response": "Alkoholgrenzwerte in Deutschland:\n• Allgemein: 0,5 Promille\n• Fahranfänger (erste 2 Jahre): 0,0 Promille\n• Unter 21 Jahren: 0,0 Promille\n• Ab 0,3 Promille bei Fahrauffälligkeiten: Strafbar\n• Empfehlung: Gar nicht trinken wenn Sie fahren müssen",
                    "intent": "alcohol_limit"
                },
                "seatbelt": {
                    "keywords": ["sicherheitsgurt", "gurt", "anschnallen", "sicherheit", "safety"],
                    "response": "Sicherheitsgurt-Vorschriften in Deutschland:\n• Fahrer und alle Mitfahrer müssen angeschnallt sein\n• Kinder benötigen altersgerechte Kindersitze\n• Vorder- und Rücksitze: Anschnallpflicht\n• Verstoß kann Bußgeld zur Folge haben\n• Sicherheitsgurte reduzieren Verletzungsrisiko um 45%",
                    "intent": "safety_requirements"
                },
                "child_safety": {
                    "keywords": ["kindersitz", "kinder", "baby", "kleinkind", "sicherheit"],
                    "response": "Kindersicherheit im Auto:\n• Rückwärtsgerichtete Sitze: Geburt bis 2 Jahre\n• Vorwärtsgerichtete Sitze: 2-4 Jahre mit Gurt\n• Sitzerhöhung: 4-8 Jahre (bis Gurt richtig sitzt)\n• Kinder unter 12 Jahren sollten hinten sitzen\n• Nach Unfall Kindersitz ersetzen",
                    "intent": "safety_requirements"
                },
                "phone_usage": {
                    "keywords": ["handy", "telefon", "smartphone", "freisprechanlage", "telefonieren", "sms"],
                    "response": "Handy-Nutzung beim Fahren:\n• Handheld-Telefonate sind verboten\n• SMS oder WhatsApp während der Fahrt sind illegal\n• Freisprecheinrichtung oder Bluetooth verwenden\n• Sprachbefehle sind sicherer als manuelle Eingabe\n• Bei Bedarf sicher anhalten und parken",
                    "intent": "safety_requirements"
                },
                "parking": {
                    "keywords": ["parken", "parkplatz", "einparken", "parallel", "parkverbot"],
                    "response": "Parkvorschriften in Deutschland:\n• Nicht vor Feuerwehrzufahrten parken\n• Behindertenparkplätze nur mit Ausweis\n• Parkscheinautomaten und Zeiten beachten\n• Einparken: Platz 1,5x Autolänge, Spiegel ausrichten, rückwärts einparken\n• Nicht vor Einfahrten oder Zebrastreifen parken",
                    "intent": "parking_regulations"
                },
                "right_of_way": {
                    "keywords": ["vorfahrt", "vorrang", "kreuzung", "rechts vor links"],
                    "response": "Vorfahrtsregeln an Kreuzungen:\n• Rechts vor Links an gleichberechtigten Kreuzungen\n• Vorfahrtstraße hat immer Vorrang\n• Linksabbieger müssen Gegenverkehr durchlassen\n• Rettungsfahrzeuge haben immer Vorfahrt\n• Fußgänger an Zebrastreifen haben Vorrang\n• Im Zweifel: Vorsicht und nachgeben",
                    "intent": "right_of_way"
                },
                "traffic_signs": {
                    "keywords": ["verkehrszeichen", "schilder", "stop", "vorfahrt", "geschwindigkeit"],
                    "response": "Wichtige Verkehrszeichen:\n• STOP-Schild: Vollständig anhalten erforderlich\n• Vorfahrt gewähren: Verlangsamen, anderen Vorrang geben\n• Geschwindigkeitsbegrenzung: Höchstgeschwindigkeit beachten\n• Parkverbot: Parken in diesem Bereich verboten\n• Schulzone: Reduzierte Geschwindigkeit bei Kindern\n• Alle Verkehrszeichen sind zu befolgen",
                    "intent": "traffic_signs"
                },
                "greeting": {
                    "keywords": ["hallo", "hi", "guten tag", "guten morgen", "hey", "hilfe", "was kannst du", "wie geht"],
                    "response": "Hallo! Ich bin Driver's Friend, Ihr Assistent für Verkehrsregeln. Ich kann Ihnen helfen bei:\n• Geschwindigkeitsbegrenzungen\n• Verkehrsregeln und -zeichen\n• Parkvorschriften\n• Sicherheitsbestimmungen\n• Alkoholgrenzwerte\n\nWelche Frage zum Fahren kann ich Ihnen beantworten?",
                    "intent": "greeting"
                },
                "farewell": {
                    "keywords": ["tschüss", "auf wiedersehen", "danke", "vielen dank", "das wars", 
                               "danke für die hilfe", "vielen dank für die hilfe", "ich schätze es", "danke vielmals", 
                               "herzlichen dank", "besten dank", "danke schön", "dankeschön", "das hat geholfen", 
                               "sehr hilfreich", "du hast mir geholfen", "das war hilfreich"],
                    "response": "Gerne geschehen! Fahren Sie sicher und fragen Sie mich jederzeit bei Verkehrsregeln. Schönen Tag noch! 🚗",
                    "intent": "farewell"
                }
            }
        }
        
        # Select language
        lang_key = "en-US"
        if language.startswith("de"):
            lang_key = "de"
        
        knowledge_base = offline_knowledge.get(lang_key, offline_knowledge["en-US"])
        
        # Score each category based on keyword matches
        category_scores = {}
        for category, data in knowledge_base.items():
            score = 0
            matched_keywords = []
            
            for keyword in data["keywords"]:
                if keyword in message_lower:
                    # Longer keywords get higher scores (more specific)
                    keyword_score = len(keyword)
                    # Exact word matches get bonus points
                    if f" {keyword} " in f" {message_lower} " or message_lower.startswith(keyword + " ") or message_lower.endswith(" " + keyword):
                        keyword_score *= 2
                    score += keyword_score
                    matched_keywords.append(keyword)
            
            if score > 0:
                category_scores[category] = {
                    "score": score,
                    "data": data,
                    "matched_keywords": matched_keywords
                }
        
        # Return the highest scoring category
        if category_scores:
            best_category = max(category_scores.keys(), key=lambda k: category_scores[k]["score"])
            best_data = category_scores[best_category]["data"]
            return {
                "response": best_data["response"],
                "intent": best_data["intent"],
                "confidence": 0.8,
                "suggestions": self._generate_related_questions(best_data["intent"], language)
            }
        
        return None
    
    async def _store_message(self, user_id: str, content: str, sender: str, **kwargs):
        """Store a message in the user's chat history"""
        # For now, store in memory. In production, this should use a database
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        message_data = {
            "content": content,
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        
        # Keep only last 20 messages to prevent memory overflow
        self.conversation_memory[user_id].append(message_data)
        if len(self.conversation_memory[user_id]) > 20:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-20:]
    
    def _get_conversation_context(self, user_id: str) -> List[Dict[str, Any]]:
        """Get recent conversation history for context"""
        return self.conversation_memory.get(user_id, [])
    
    def _add_contextual_elements(self, response: str, context: List[Dict[str, Any]], language: str) -> str:
        """Add contextual elements to response based on conversation history"""
        if not context:
            return response
        
        # Get recent topics from conversation
        recent_topics = []
        for msg in context[-5:]:  # Look at last 5 messages
            if msg["sender"] == "user":
                # Extract topics from user messages
                user_message = msg["content"].lower()
                if any(keyword in user_message for keyword in ["speed", "limit", "schnell"]):
                    recent_topics.append("speed limits")
                elif any(keyword in user_message for keyword in ["parking", "park", "parken"]):
                    recent_topics.append("parking")
                elif any(keyword in user_message for keyword in ["alcohol", "drink", "alkohol"]):
                    recent_topics.append("alcohol limits")
                elif any(keyword in user_message for keyword in ["seatbelt", "belt", "gurt"]):
                    recent_topics.append("seatbelt safety")
        
        # Add contextual reference if farewell and recent topics exist
        if recent_topics and any(keyword in response.lower() for keyword in ["welcome", "gerne"]):
            if language.startswith("de"):
                context_note = f" Ich hoffe, die Informationen zu {', '.join(recent_topics)} waren hilfreich."
            else:
                context_note = f" I hope the information about {', '.join(recent_topics)} was helpful."
            response = response.replace("🚗", context_note + " 🚗")
        
        return response
