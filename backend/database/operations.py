from pymongo import MongoClient
from backend.models.regulation import Regulation

class DatabaseOperations:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['driving_regulations']
        
    def insert_regulation(self, regulation: Regulation):
        return self.db.regulations.insert_one(regulation.__dict__)
        
    def get_regulation(self, category: str, language: str):
        return self.db.regulations.find_one({
            'category': category,
            'language': language
        })