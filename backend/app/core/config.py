import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL : str = os.getenv("DATABASE_URL", "sqlite:///./database.db")

    SECRET_KEY : str = os.getenv("SECRET_KEY")

    ALLOWED_ORIGINS: List[str]

    FIREBASE_KEY_PATH : str = os.getenv("FIREBASE_KEY_PATH")
    
    class Config:
        env_file = ".env"

settings = Settings()

print(settings.FIREBASE_KEY_PATH)
