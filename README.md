# 🚗 Driver's Friend - Multilingual Driving Regulations Chatbot

A comprehensive AI-powered chatbot designed to help users understand German driving rules and regulations. Features intelligent web scraping, offline knowledge base, conversation memory, and full bilingual support (English/German).

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![React](https://img.shields.io/badge/React-18.3+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)

## 🌟 Features

### 🤖 **Advanced AI Chat System**
- **Natural Language Processing** with spaCy (English & German models)
- **Conversation Memory** - Remembers context within chat sessions
- **Enhanced Thank You Detection** - Contextual farewell responses in both languages
- **Intent Classification** - Smart categorization of user queries

### 🌐 **Intelligent Information Sources**
- **Offline Knowledge Base** - Comprehensive German driving regulations
- **Dual Web Scraping** - Real-time data from RouteToGermany.com and GettingAroundGermany.info
- **Smart Source Selection** - Automatically chooses most relevant information source
- **MongoDB Integration** - Persistent storage for regulations and chat history

### 🗣️ **Multilingual Support**
- **Full German Localization** - Native German responses with priority over web content
- **Language-Aware Processing** - Context-sensitive responses based on user language
- **Seamless Language Switching** - Dynamic language detection and response formatting

### 🎨 **Modern User Interface**
- **Material-UI Design** - Clean, responsive interface
- **Real-time Chat** - Instant responses with typing indicators
- **Firebase Authentication** - Secure user management (with demo mode)
- **TypeScript Frontend** - Type-safe React application

## 🏗️ **Technology Stack**

### Backend
- **FastAPI** - High-performance Python web framework
- **MongoDB** - Document database for regulations storage
- **spaCy** - Advanced NLP processing
- **BeautifulSoup** - Web scraping capabilities
- **Uvicorn** - ASGI server for production deployment

### Frontend
- **React 18** - Modern frontend framework
- **TypeScript** - Type-safe JavaScript
- **Material-UI** - Google's Material Design components
- **Axios** - HTTP client for API communication
- **React i18next** - Internationalization support

### Infrastructure
- **Docker & Docker Compose** - Containerized deployment
- **Virtual Environment** - Isolated Python dependencies
- **CORS Middleware** - Cross-origin request handling

## 📋 **Prerequisites**

Before starting, ensure you have the following installed:

- **Python 3.11+** 
- **Node.js 16+** and **npm**
- **MongoDB** (or use Docker)
- **Git**
- **Docker & Docker Compose** (optional, for containerized deployment)

## 🚀 **Quick Start Guide**

### Option 1: Manual Setup (Recommended for Development)

#### 1. **Clone the Repository**
```bash
git clone https://github.com/debanjanofficial/Driver-s-Friend.git
cd Driver-s-Friend
```

#### 2. **Backend Setup**
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy language models
python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm

# Start MongoDB (if not using Docker)
# Make sure MongoDB is running on localhost:27017

# Initialize the database with sample data
python check_db.py

# Start the backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 3. **Frontend Setup**
```bash
# Open new terminal and navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm start
```

#### 4. **Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Option 2: Docker Deployment

#### 1. **Using Docker Compose**
```bash
# Clone the repository
git clone https://github.com/debanjanofficial/Driver-s-Friend.git
cd Driver-s-Friend

# Start all services with Docker Compose
docker-compose up --build

# Access the application at http://localhost:3000
```

## 📚 **Usage Examples**

### English Queries
```
👤 "What are the speed limits in Germany?"
🤖 "Speed limits in Germany vary by road type: Urban areas: 50 km/h, Rural roads: 100 km/h, Autobahn: No general limit (130 km/h recommended)..."

👤 "Thanks for your help!"
🤖 "You're welcome! I hope the information about speed limits was helpful. Drive safely! 🚗"
```

### German Queries
```
👤 "Wie hoch ist die Promillegrenze in Deutschland?"
🤖 "Die Promillegrenze in Deutschland beträgt 0,5 Promille für erfahrene Fahrer und 0,0 Promille für Fahranfänger..."

👤 "Vielen Dank für die Hilfe!"
🤖 "Gerne geschehen! Ich hoffe, die Informationen zu Alkoholgrenzwerte waren hilfreich. Fahren Sie sicher! 🚗"
```

## 🛠️ **Development**

### **Backend Development**
```bash
# Activate virtual environment
source .venv/bin/activate

# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests (if available)
python -m pytest
```

### **Frontend Development**
```bash
# Install dependencies
npm install

# Start development server with hot reload
npm start

# Build for production
npm run build

# Run tests
npm test
```

### **Database Management**
```bash
# Check database connection and sample data
cd backend
python check_db.py

# View database contents
python -c "
from app.database.operations import DatabaseOperations
db = DatabaseOperations()
print('Regulations count:', db.collection.count_documents({}))
"
```

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the project root:
```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DB_NAME=driving_rules

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Firebase Configuration (optional)
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
```

### **Language Models**
The system requires spaCy language models:
```bash
# English model
python -m spacy download en_core_web_sm

# German model  
python -m spacy download de_core_news_sm
```

## 🧪 **Testing the System**

### **API Testing**
```bash
# Test the chat endpoint
curl -X POST "http://localhost:8000/api/chat" \
-H "Content-Type: application/json" \
-d '{"message": "What are parking rules?", "user_id": "test", "language": "en"}'

# Test German language
curl -X POST "http://localhost:8000/api/chat" \
-H "Content-Type: application/json" \
-d '{"message": "Wie sind die Parkregeln?", "user_id": "test", "language": "de"}'
```

### **Feature Testing Checklist**
- [ ] English queries return comprehensive responses
- [ ] German queries return native German responses
- [ ] Thank you messages trigger contextual farewell responses
- [ ] Conversation memory works across multiple messages
- [ ] Web scraping provides fallback information
- [ ] Language switching works seamlessly

## 📱 **API Endpoints**

### **Chat API**
- **POST** `/api/chat` - Process chat messages
  ```json
  {
    "message": "Your question here",
    "user_id": "optional_user_id", 
    "language": "en" // or "de"
  }
  ```

### **Search API**
- **GET** `/api/search` - Search regulations database
- **POST** `/api/search` - Advanced search with filters

### **Utilities**
- **GET** `/health` - Health check endpoint
- **GET** `/docs` - Interactive API documentation

## 🤝 **Contributing**

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### **Development Guidelines**
- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Add comments for complex logic
- Update documentation for new features
- Test both English and German functionality

## 🐛 **Troubleshooting**

### **Common Issues**

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000  
lsof -ti:3000 | xargs kill -9
```

**MongoDB connection issues:**
```bash
# Start MongoDB service
brew services start mongodb/brew/mongodb-community
# Or on Linux: sudo systemctl start mongod
```

**spaCy model not found:**
```bash
# Reinstall language models
python -m spacy download en_core_web_sm --force
python -m spacy download de_core_news_sm --force
```

**Virtual environment issues:**
```bash
# Recreate virtual environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Authors**

- **Debanjan** - *Initial work* - [@debanjanofficial](https://github.com/debanjanofficial)

## 🙏 **Acknowledgments**

- spaCy team for excellent NLP tools
- Material-UI for beautiful React components
- MongoDB for reliable document storage
- FastAPI for high-performance web framework
- The German driving regulations sources

---

**Drive safely and ask away! 🚗💨**
