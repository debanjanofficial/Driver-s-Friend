class ResponseGenerator:
    def __init__(self, db_connection):
        self.db = db_connection
        
    def generate_response(self, intent, language):
        regulation = self.db.regulations.find_one({
            'intent': intent,
            'language': language
        })
        return regulation['response'] if regulation else "I'm sorry, I don't have that information."
