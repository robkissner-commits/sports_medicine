from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./sports_medicine.db"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Application
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
