from pydantic_settings import BaseSettings
from pydantic import ConfigDict
class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "driving_regulations"
    debug: bool = True
    
    model_config = ConfigDict(
        extra='allow',  # Allow extra fields
        env_file='.env'
    )

settings = Settings()
