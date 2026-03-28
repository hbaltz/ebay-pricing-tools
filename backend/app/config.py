"""Application configuration loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings sourced from environment variables or a .env file.

    Attributes:
        ebay_app_id: eBay Developer App ID (Client ID).
        ebay_environment: Target eBay API environment.
    """

    ebay_app_id: str = Field(..., description="eBay Developer App ID (Client ID)")
    ebay_environment: Literal["production", "sandbox"] = Field(
        "sandbox",
        description="'sandbox' for development, 'production' for live data",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance.

    Returns:
        The singleton Settings instance loaded from the environment.
    """
    return Settings()
