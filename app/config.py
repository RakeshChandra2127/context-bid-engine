from functools import lru_cache
from typing import Literal, Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    # Application
    APP_NAME: str = "AdContext Engine"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./adcontext.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 3600

    # AI Provider
    AI_PROVIDER: Literal["openai", "anthropic"] = "openai"
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-4o-mini"
    AI_TIMEOUT_SECONDS: int = 10

    # Auction
    AUCTION_SECOND_PRICE: bool = True
    MIN_RELEVANCE_SCORE: float = 0.3

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @model_validator(mode="after")
    def validate_api_keys(self) -> "Settings":
        """Validate that the appropriate API key is set for the chosen provider."""
        if self.AI_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when AI_PROVIDER is 'openai'")
        if self.AI_PROVIDER == "anthropic" and not self.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY is required when AI_PROVIDER is 'anthropic'"
            )
        return self


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
