import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL : str = os.getenv("DATABASE_URL", "sqlite:///./database.db")

    SECRET_KEY : str = os.getenv("SECRET_KEY")

    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

    FIREBASE_KEY_PATH : str = os.getenv("FIREBASE_KEY_PATH")
    
    class Config:
        env_file = ".env"

settings = Settings()

print(settings.FIREBASE_KEY_PATH)
