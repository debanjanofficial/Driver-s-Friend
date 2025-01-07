from app.database.operations import DatabaseOperations

def setup_database():
    db_ops = DatabaseOperations()
    # Example: create indexes, insert seed data, etc.
    db_ops.db.regulations.create_index([("category", 1)])
    db_ops.db.regulations.create_index([("language", 1)])
    print("Database setup completed.")

if __name__ == "__main__":
    setup_database()
