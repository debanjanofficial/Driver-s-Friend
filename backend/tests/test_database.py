# backend/tests/test_database.py
import pytest
from database.operations import DatabaseOperations
from models.regulation import Regulation

def test_database_connection():
    db_ops = DatabaseOperations()
    assert db_ops.client.server_info() is not None

def test_regulation_insertion():
    db_ops = DatabaseOperations()
    regulation = Regulation(
        category="test",
        country="germany",
        content="Test regulation",
        language="en-US",
        keywords=["test"],
        last_updated=datetime.now(),
        source="Test"
    )
    result = db_ops.insert_regulation(regulation)
    assert result.inserted_id is not None
