from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    APP_NAME: str = "PetCare API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API para gestionar tus mascotas y sus pendientes 🐾"

    SECRET_KEY: str = "super-secret-key-change-in-production-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas

    DATABASE_URL: str = "sqlite:///./petcare.db"

    class Config:
        env_file = ".env"


settings = Settings()
