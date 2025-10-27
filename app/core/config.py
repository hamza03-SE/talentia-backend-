# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Talentia"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    DATABASE_URL: str
    API_PREFIX: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 jour
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    # SMTP
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    FRONTEND_URL: str

    class Config:
        # Chemin absolu vers .env à la racine du projet
        env_file = str(Path(__file__).resolve().parents[2] / ".env")
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()