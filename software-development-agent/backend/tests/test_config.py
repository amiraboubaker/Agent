import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_production_requires_llm_key() -> None:
    with pytest.raises(ValidationError):
        Settings(app_env="production", llm_api_key="")


def test_llm_url_requires_approved_https_host() -> None:
    settings = Settings(llm_api_key="test-key", llm_api_url="http://localhost:8000")
    with pytest.raises(ValueError):
        settings.validate_llm_url()