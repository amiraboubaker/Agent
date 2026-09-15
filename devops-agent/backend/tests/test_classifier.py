from app.agents.classifier import classify_task


def test_classifies_deployment_request() -> None:
    assert classify_task("Deploy this Docker Compose app to a VPS") == "deployment"


def test_classifies_security_request() -> None:
    assert classify_task("Configure SSL and harden the server") == "security"


def test_defaults_to_general_infrastructure() -> None:
    assert classify_task("Help me understand this environment") == "general_infrastructure"
