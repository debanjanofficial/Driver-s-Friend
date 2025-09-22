import uvicorn
from fastapi import FastAPI
from app.config import settings
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Driving Regulations Chatbot")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins like ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include all your API endpoints from routes.py
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",    # "module:variable"
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
