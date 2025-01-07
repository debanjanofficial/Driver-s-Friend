import uvicorn
from fastapi import FastAPI
from api.routes import router
from config import settings

app = FastAPI(title="Driving Regulations Chatbot")
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )