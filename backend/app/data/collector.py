from pymongo import MongoClient
import os
from datetime import datetime

class DataCollector:
    def __init__(self):
        self.db = MongoClient(os.getenv('MONGODB_URI'))
        
    def store_regulation(self, country, category, rule):
        return self.db.regulations.insert_one({
            'country': country,
            'category': category,
            'rule': rule,
            'timestamp': datetime.now()
        })