"""
Configuration management using environment variables
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "SME Financial Compass"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "https://sme-financial-compass.vercel.app/"
    ]
    
    # Database (Supabase)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # OpenRouter API (for LLM)
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL: str = "openai/gpt-4-turbo-preview"  # or "anthropic/claude-3-opus"
    FALLBACK_MODEL: str = "openai/gpt-3.5-turbo"
    
    # Banking APIs
    PLAID_CLIENT_ID: str = os.getenv("PLAID_CLIENT_ID", "")
    PLAID_SECRET: str = os.getenv("PLAID_SECRET", "")
    PLAID_ENV: str = os.getenv("PLAID_ENV", "sandbox")  # sandbox, development, production
    
    RAZORPAY_KEY_ID: str = os.getenv("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.getenv("RAZORPAY_KEY_SECRET", "")
    
    # GST API (optional)
    GST_API_KEY: str = os.getenv("GST_API_KEY", "")
    GST_API_URL: str = os.getenv("GST_API_URL", "")
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".csv", ".xlsx", ".xls", ".pdf"]
    UPLOAD_DIR: str = "uploads"
    
    # Redis (for caching - optional)
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    
    # Supported Languages
    SUPPORTED_LANGUAGES: List[str] = ["en", "hi", "te", "ta", "kn", "mr", "gu", "bn"]
    DEFAULT_LANGUAGE: str = "en"
    
    # Industry Benchmarks
    SUPPORTED_INDUSTRIES: List[str] = [
        "manufacturing",
        "retail",
        "agriculture",
        "services",
        "logistics",
        "ecommerce",
        "healthcare",
        "construction",
        "hospitality",
        "technology"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
