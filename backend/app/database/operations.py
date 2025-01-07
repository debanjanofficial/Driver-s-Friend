from pymongo import MongoClient
import os
from datetime import datetime
from app.config import settings

class DatabaseOperations:
    def __init__(self):
        self.client = MongoClient(settings.mongodb_uri)
        self.db = self.client[settings.database_name]

    def get_regulations(self, category: str, language: str):
        return list(self.db.regulations.find(
            {"category": category, "language": language}, {"_id": 0}
        ))

    def insert_regulation(self, regulation_data: dict):
        return self.db.regulations.insert_one(regulation_data).inserted_id

    def log_chat_interaction(self, user_id: str, message: str,
                             intent: str, response: str):
        return self.db.chat_logs.insert_one({
            "user_id": user_id,
            "message": message,
            "intent": intent,
            "response": response,
            "timestamp": datetime.utcnow()
        })
