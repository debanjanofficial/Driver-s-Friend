from pymongo import MongoClient
from typing import List, Optional
from app.config import settings  # or wherever your config is stored

class DatabaseOperations:
    def __init__(self):
        # Connect to MongoDB using your config
        self.client = MongoClient(settings.mongodb_uri)
        self.db = self.client[settings.database_name]

    def search_regulations(self, keywords, language="en-US"):
        """
        Search for rules that match any of the keywords and the specified language.
        """
        query = {
            "$and": [
                {"keywords": {"$in": keywords}},  # Matches any keyword
                {"language": {"$regex": language}} 
                # Example: if your 'language' field is "[en-US], [en-GB], [en-IN]",
                # you can use a regex to match "en-US"
            ]
        }
        return list(self.db.regulations.find(query, {"_id": 0}))
    def get_regulations(self, category: str, language: str = "en-US") -> List[dict]:
        """
        Get regulations by category and language
        """
        query = {
            "$and": [
                {"category": category},
                {"language": {"$regex": language}}
            ]
        }
        return list(self.db.regulations.find(query, {"_id": 0}))
    def insert_regulation(self, regulations: List[dict]) -> None:
        """
        Insert new regulations into the database
        """
        if isinstance(regulations, list):
            self.db.regulations.insert_many(regulations)
        else:
            self.db.regulations.insert_one(regulations)
            
    def insert_regulation(self, regulations: List[dict]) -> None:
        """
        Insert new regulations into the database
        """
        if isinstance(regulations, list):
            self.db.regulations.insert_many(regulations)
        else:
            self.db.regulations.insert_one(regulations)
            
    def store_chat_message(self, message_data):
        return self.db.chat_history.insert_one(message_data)
    
    def get_chat_history(self, user_id, limit=10):
        return list(self.db.chat_history.find(
        {"user_id": user_id}, 
        {"_id": 0}
        ).sort("timestamp", -1).limit(limit))
    
    def get_categories(self, language: str = "en-US") -> List[str]:
        """
        Get all available categories for a specific language
        """
        pipeline = [
            {"$match": {"language": {"$regex": language}}},
            {"$group": {"_id": "$category"}},
            {"$sort": {"_id": 1}}
        ]
        result = list(self.db.regulations.aggregate(pipeline))
        return [item["_id"] for item in result]