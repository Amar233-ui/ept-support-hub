from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration, read from environment variables prefixed with AI_."""

    model_config = SettingsConfigDict(env_prefix="AI_", env_file=".env", extra="ignore")

    env: str = "dev"
    database_url: str = "postgresql://supporthub:supporthub@localhost:5432/supporthub"
    # Shared secret the backend sends in X-Internal-Token; the service is never public.
    internal_token: str = "change-me-dev-only"
    models_cache_dir: str = "/models-cache"


@lru_cache
def get_settings() -> Settings:
    return Settings()
