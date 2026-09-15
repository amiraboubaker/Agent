from app.agents.classifier import classify_task


def test_classifies_vulnerability_request() -> None:
    assert classify_task("Audit this API for OWASP injection vulnerabilities") == "vulnerability_analysis"


def test_classifies_secure_implementation_request() -> None:
    assert classify_task("Recommend secure authentication and secrets management") == "secure_implementation"


def test_defaults_to_general_security() -> None:
    assert classify_task("Help me review this service") == "general_security"
