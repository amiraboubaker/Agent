from app.agents.classifier import classify_task


def test_classifies_discovery_request() -> None:
    assert classify_task("Interview target users to understand their needs") == "discovery"


def test_classifies_validation_request() -> None:
    assert classify_task("Design an experiment to validate our riskiest hypothesis") == "validation"


def test_defaults_to_general_product() -> None:
    assert classify_task("Help me shape this idea") == "general_product"
