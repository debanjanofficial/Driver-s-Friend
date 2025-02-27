# Driver-s-Friend
A multilingual chatbot designed to answer questions related to driving rules, regulations, and fines in Germany. The chatbot uses a React frontend, a FastAPI backend, and MongoDB as the database to store driving-related rules.

## Table of Contents
1) Project Description
2) Installation
3) Usage
4) Contributing
5) License
## Project Description
The Driver's Friend Chatbot is an interactive system that allows users to ask questions about driving regulations in Germany. It supports multiple languages (English and German) and provides accurate answers by querying a MongoDB database that stores detailed driving rules. The chatbot processes user queries using natural language processing (NLP) techniques, tokenizes the input, and fetches relevant information from the database.

## Features
1) Multilingual support (English and German).
2) Real-time chat interface with Material UI.
3) Backend processes user queries using tokenization and retrieves answers from the database.
4) Database stores driving rules categorized by type (e.g., speed limits, alcohol limits).
5) Responsive design using Material UI.

## Installation
To install the necessary packages, follow the instructions below:

### Backend
sh
pip install -r requirements.txt
### Frontend
sh
npm install
## Usage
To run the project, use the following commands:

### Backend
sh
python manage.py runserver
### Frontend
sh
npm start
## Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
## License
This project is licensed under the MIT License. See the LICENSE file for details.
