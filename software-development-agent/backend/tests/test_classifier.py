from app.agents.classifier import classify_task


def test_classifies_debugging_request() -> None:
    assert classify_task("Why does this traceback happen?") == "debugging"


def test_classifies_testing_request() -> None:
    assert classify_task("Create pytest coverage for this service") == "testing"


def test_defaults_to_coding() -> None:
    assert classify_task("Build a small feature") == "coding"
