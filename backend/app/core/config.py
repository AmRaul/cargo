from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Cargo Shipping API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database - required from .env
    DATABASE_URL: str

    # Security - required from .env (no defaults for security!)
    SECRET_KEY: str
    ADMIN_PASSWORD: str

    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
