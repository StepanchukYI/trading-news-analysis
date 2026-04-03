"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    database_url: str = "postgresql://localhost/trading_news"
    redis_url: str = "redis://localhost/2"
    log_level: str = "INFO"

    class Config:
        env_prefix = "NEWS_"


settings = Settings()
