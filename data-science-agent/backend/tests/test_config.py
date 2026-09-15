import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_production_requires_llm_key() -> None:
    with pytest.raises(ValidationError):
        Settings(app_env="production", llm_api_key="")


def test_local_ollama_url_is_allowed_without_api_key() -> None:
    settings = Settings(llm_api_url="http://localhost:11434/v1/chat/completions")
    settings.validate_llm_url()
    assert settings.is_local_llm


def test_docker_ollama_url_is_allowed_without_api_key() -> None:
    settings = Settings(llm_api_url="http://host.docker.internal:11434/v1/chat/completions")
    settings.validate_llm_url()
    assert settings.is_local_llm


def test_remote_llm_url_requires_https() -> None:
    settings = Settings(
        llm_api_key="test-key",
        llm_api_url="http://api.openai.com/v1/chat/completions",
    )
    with pytest.raises(ValueError):
        settings.validate_llm_url()