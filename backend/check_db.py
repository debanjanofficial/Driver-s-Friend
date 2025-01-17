from app.database.operations import DatabaseOperations
from datetime import datetime
from pymongo import MongoClient

db_ops = DatabaseOperations()

# Insert sample regulation for speed limits
sample_regulation = [{
    "category": "speed_limit",
    "country": "germany",
    "content": "The speed limit in urban areas is 50 km/h.",
    "language": ["en-US", "en-GB", "en-I"],
    "keywords": ["speed", "urban", "limit"],
    "last_updated": datetime.now(),
    "source": "StVO §3",
    "fine_amount": 50.0
},
{
    
        "category": "alcohol_limit",
        "country": "germany",
        "content": "The legal alcohol limit for drivers is 0.5‰.",
        "language": "en-US",
        "keywords": ["alcohol", "limit", "drivers"],
        "last_updated": datetime.now(),
        "source": "StVO §24a",
        "fine_amount": 500.0,
    

}]

db_ops.insert_regulation(sample_regulation)
print("Sample regulation inserted.")
