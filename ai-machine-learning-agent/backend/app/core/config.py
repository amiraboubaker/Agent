from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_env: str = "development"
    llm_api_url: str = "http://localhost:11434/v1/chat/completions"
    llm_api_key: str = ""
    llm_model: str = "llama3.2"
    database_url: str = "sqlite:///./data/agent.db"
    cors_origins: str = "http://localhost:5173"
    llm_allowed_hosts: str = "localhost,127.0.0.1,host.docker.internal,api.openai.com"
    rate_limit_per_minute: int = 20

    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", extra="ignore")

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if self.app_env.lower() == "production" and not self.llm_api_key:
            raise ValueError("LLM_API_KEY must be configured in production")
        if self.rate_limit_per_minute < 1:
            raise ValueError("RATE_LIMIT_PER_MINUTE must be at least 1")
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def llm_allowed_host_list(self) -> list[str]:
        return [host.strip().lower() for host in self.llm_allowed_hosts.split(",") if host.strip()]

    @property
    def is_local_llm(self) -> bool:
        parsed = urlparse(self.llm_api_url)
        return parsed.hostname in {"localhost", "127.0.0.1", "host.docker.internal"}

    def validate_llm_url(self) -> None:
        parsed = urlparse(self.llm_api_url)
        if parsed.hostname not in self.llm_allowed_host_list:
            raise ValueError("LLM_API_URL must use an approved provider host")
        if not self.is_local_llm and parsed.scheme != "https":
            raise ValueError("Remote LLM_API_URL values must use HTTPS")


@lru_cache
def get_settings() -> Settings:
    return Settings()
