import uvicorn
from fastapi import FastAPI
from app.config import settings
from app.api.routes import router

app = FastAPI(title="Driving Regulations Chatbot")

# Include all your API endpoints from routes.py
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",    # "module:variable"
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
