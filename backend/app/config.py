from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "driving_regulations"
    MODEL_PATH: str = "models"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
