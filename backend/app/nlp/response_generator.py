"""
Generates a response based on the predicted intent and queries 
the database for corresponding regulation information.
"""
from app.database.operations import DatabaseOperations

class ResponseGenerator:
    def __init__(self, db_ops: DatabaseOperations):
        """
        Args:
            db_ops (DatabaseOperations): An instance of a database operation class 
                                         to handle queries.
        """
        self.db_ops = db_ops

    def generate_response(self, intent_name: str, language: str) -> str:
        """
        Fetch a regulation or answer from the 'regulations' collection
        based on the user's intent and language.

        Args:
            intent_name (str): The predicted intent (e.g. 'speed_limit').
            language   (str): A language code (e.g. 'en-US', 'de').

        Returns:
            str: A suitable response message or a fallback.
        """
        # We assume 'get_regulations' takes 'category' and 'language'
        # and returns a list of regulation docs. 
        data = self.db_ops.get_regulations(category=intent_name, language=language)
        if data and len(data) > 0:
            # For simplicity, return the "content" field of the first matching record.
            return data[0].get("content", "No content found for this intent.")
        
        # Fallback: No relevant data found
        return "I don't have information on that right now."
