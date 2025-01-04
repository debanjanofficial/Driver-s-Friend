# backend/database/operations.py
from pymongo import MongoClient
from typing import List, Optional
import os

class DatabaseOperations:
    def __init__(self):
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.client = MongoClient(mongodb_uri)
        self.db = self.client['driving_regulations']
    
    def get_regulations(self, category: str, language: str) -> List[dict]:
        return list(self.db.regulations.find(
            {"category": category, "language": language},
            {"_id": 0}
        ))
    
    def log_chat_interaction(self, user_id: str, message: str, 
                           intent: str, response: str):
        return self.db.chat_logs.insert_one({
            "user_id": user_id,
            "message": message,
            "intent": intent,
            "response": response,
            "timestamp": datetime.utcnow()
        })
