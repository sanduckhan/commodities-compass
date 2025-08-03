from typing import List
from pydantic_settings import BaseSettings
from decouple import config
import json


class Settings(BaseSettings):
    # Application
    APP_NAME: str = config("APP_NAME", default="Commodities Compass")
    APP_VERSION: str = config("APP_VERSION", default="1.0.0")
    API_V1_STR: str = config("API_V1_STR", default="/v1")
    DEBUG: bool = config("DEBUG", default=False, cast=bool)
    BACKEND_PORT: int = config("BACKEND_PORT", default=8000, cast=int)

    # Auth0
    AUTH0_DOMAIN: str = config("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID: str = config("AUTH0_CLIENT_ID")
    AUTH0_API_AUDIENCE: str = config("AUTH0_API_AUDIENCE")
    AUTH0_ALGORITHMS: List[str] = config("AUTH0_ALGORITHMS", default="RS256").split(",")
    AUTH0_ISSUER: str = config("AUTH0_ISSUER")

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Handle CORS origins from environment
        cors_origins = config(
            "BACKEND_CORS_ORIGINS",
            default='["http://localhost:5173", "http://localhost:3000"]',
        )
        if isinstance(cors_origins, str):
            try:
                # Try to parse as JSON array first
                self.BACKEND_CORS_ORIGINS = json.loads(cors_origins)
            except json.JSONDecodeError:
                # Fall back to comma-separated string
                self.BACKEND_CORS_ORIGINS = [
                    origin.strip() for origin in cors_origins.split(",")
                ]

    # Database
    DATABASE_URL: str = config("DATABASE_URL")
    DATABASE_SYNC_URL: str = config("DATABASE_SYNC_URL")

    # Redis
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379/0")

    # Google Sheets
    GOOGLE_SHEETS_CREDENTIALS_PATH: str = config(
        "GOOGLE_SHEETS_CREDENTIALS_PATH", default=""
    )
    SPREADSHEET_ID: str = config("SPREADSHEET_ID")

    # External APIs
    WEATHER_API_KEY: str = config("WEATHER_API_KEY", default="")
    NEWS_API_KEY: str = config("NEWS_API_KEY", default="")

    # AWS Configuration
    AWS_ACCESS_KEY_ID: str = config("AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY: str = config("AWS_SECRET_ACCESS_KEY", default="")
    AWS_REGION: str = config("AWS_REGION", default="us-east-1")
    S3_BUCKET_NAME: str = config("S3_BUCKET_NAME", default="")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
