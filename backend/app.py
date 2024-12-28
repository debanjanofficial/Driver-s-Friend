from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data['query']
    language = data['language']
    
    response = chatbot.process(query, language)
    return jsonify(response)