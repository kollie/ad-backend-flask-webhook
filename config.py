import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent
    
    # Database
    SQLALCHEMY_DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db"  # Default SQLite database
    )
    
    # JWT settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-keep-it-secret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # CORS settings
    CORS_ORIGINS = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
    ]