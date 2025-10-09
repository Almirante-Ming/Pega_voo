from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseModel):
    """Application settings for environment variable management"""
    
    # Database Configuration
    database_url: str = Field(
        default_factory=lambda: os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/task_fly_db"),
        description="Database connection URL"
    )
    
    # JWT Configuration
    secret_key: str = Field(
        default_factory=lambda: os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production"),
        description="Secret key for JWT token generation"
    )
    algorithm: str = Field(
        default_factory=lambda: os.getenv("ALGORITHM", "HS256"),
        description="JWT algorithm"
    )
    access_token_expire_minutes: int = Field(
        default_factory=lambda: int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
        description="JWT token expiration time in minutes"
    )
    
    # API Configuration
    api_host: str = Field(
        default_factory=lambda: os.getenv("API_HOST", "0.0.0.0"),
        description="API host"
    )
    api_port: int = Field(
        default_factory=lambda: int(os.getenv("API_PORT", "8000")),
        description="API port"
    )
    api_reload: bool = Field(
        default_factory=lambda: os.getenv("API_RELOAD", "true").lower() == "true",
        description="Enable auto-reload for development"
    )
    
    # CORS Configuration
    cors_origins: List[str] = Field(
        default_factory=lambda: (
            os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080,http://localhost:4200")
            .split(",") if os.getenv("CORS_ORIGINS") else 
            ["http://localhost:3000", "http://localhost:8080", "http://localhost:4200"]
        ),
        description="CORS allowed origins"
    )
    
    # Environment
    environment: str = Field(
        default_factory=lambda: os.getenv("ENVIRONMENT", "development"),
        description="Application environment"
    )
    debug: bool = Field(
        default_factory=lambda: os.getenv("DEBUG", "true").lower() == "true",
        description="Enable debug mode"
    )
    
    # Logging
    log_level: str = Field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"),
        description="Logging level"
    )


# Create a global settings instance
settings = Settings()