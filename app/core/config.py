from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    # -------------------------
    # Database
    # -------------------------
    DATABASE_URL: str

    # -------------------------
    # JWT
    # -------------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # -------------------------
    # CORS
    # -------------------------
    CORS_ALLOW_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
