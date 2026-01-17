"""Application configuration using pydantic-settings."""

from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = "ParagonStats"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./data/paragonstats.db"

    # Storage
    raw_receipts_path: Path = Path("./storage/raw_receipts")

    # BuyCoffee
    buycoffee_url: str = "https://buycoffee.to/your-profile"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Streamlit
    streamlit_port: int = 8501

    @property
    def db_path(self) -> Path:
        """Extract SQLite database file path from URL."""
        # sqlite:///./data/paragonstats.db -> ./data/paragonstats.db
        return Path(self.database_url.replace("sqlite:///", ""))


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
