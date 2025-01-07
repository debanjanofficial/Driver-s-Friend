from pymongo import MongoClient
from datetime import datetime

class DatabaseSetup:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['driving_regulations']
        
    def create_collections(self):
        # Create collections if they don't exist
        self.db.create_collection('regulations')
        self.db.create_collection('user_queries')
        
    def create_indexes(self):
        # Create indexes for faster queries
        self.db.regulations.create_index([('country', 1)])
        self.db.regulations.create_index([('category', 1)])
        self.db.regulations.create_index([('language', 1)])

# Initial setup script
if __name__ == "__main__":
    setup = DatabaseSetup()
    setup.create_collections()
    setup.create_indexes()
