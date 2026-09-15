from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    llm_api_url: str = "http://localhost:11434/v1/chat/completions"
    llm_api_key: str = ""
    llm_model: str = "llama3.2"
    cors_origins: str = "http://localhost:5174"
    llm_allowed_hosts: str = "localhost,127.0.0.1,api.openai.com"
    rate_limit_per_minute: int = 20
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_local_llm(self) -> bool:
        return self.llm_api_url.startswith("http://localhost") or self.llm_api_url.startswith("http://127.0.0.1")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
