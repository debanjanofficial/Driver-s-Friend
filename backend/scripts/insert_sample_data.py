from backend.database.operations import DatabaseOperations
from backend.models.regulation import Regulation
from datetime import datetime

def insert_sample_regulations():
    db_ops = DatabaseOperations()
    
    # Sample speed limit regulation
    speed_limit = Regulation(
        category="speed_limits",
        country="germany",
        content="In urban areas, the speed limit is 50 km/h",
        language="en-US",
        keywords=["speed", "urban", "limit"],
        last_updated=datetime.now(),
        source="StVO §3",
        fine_amount=50.0
    )
    
    db_ops.insert_regulation(speed_limit)

if __name__ == "__main__":
    insert_sample_regulations()