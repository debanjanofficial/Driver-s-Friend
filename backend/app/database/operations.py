from pymongo import MongoClient
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
