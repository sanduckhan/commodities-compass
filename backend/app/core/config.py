from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
from decouple import config


class Settings(BaseSettings):
    # Application
    APP_NAME: str = config("APP_NAME", default="Commodities Compass")
    APP_VERSION: str = config("APP_VERSION", default="1.0.0")
    API_V1_STR: str = config("API_V1_STR", default="/api/v1")
    DEBUG: bool = config("DEBUG", default=False, cast=bool)

    # Auth0
    AUTH0_DOMAIN: str = config("AUTH0_DOMAIN")
    AUTH0_API_AUDIENCE: str = config("AUTH0_API_AUDIENCE")
    AUTH0_ALGORITHMS: List[str] = config("AUTH0_ALGORITHMS", default="RS256").split(",")
    AUTH0_ISSUER: str = config("AUTH0_ISSUER")

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

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

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
