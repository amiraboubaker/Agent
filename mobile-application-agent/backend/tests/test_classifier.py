from app.agents.classifier import classify_task


def test_classifies_navigation_request() -> None:
    assert classify_task("Design a tab and stack navigation flow") == "navigation"


def test_classifies_mobile_api_request() -> None:
    assert classify_task("Add authentication and REST API integration") == "api_integration"


def test_defaults_to_general_mobile() -> None:
    assert classify_task("Help me plan my app") == "general_mobile"
