from app.agents.classifier import classify_task


def test_classifies_frontend_request() -> None:
    assert classify_task("Build a responsive React and TypeScript dashboard") == "frontend"


def test_classifies_backend_request() -> None:
    assert classify_task("Secure the Express API with authentication") == "backend"


def test_defaults_to_general_web() -> None:
    assert classify_task("Help me plan a new web application") == "general_web"
