from app.agents.classifier import classify_task


def test_classifies_research_request() -> None:
    assert classify_task("Plan user interviews and usability research") == "ux_research"


def test_classifies_accessibility_request() -> None:
    assert classify_task("Audit keyboard navigation and WCAG contrast") == "accessibility"


def test_defaults_to_general_design() -> None:
    assert classify_task("Help me improve this digital product") == "general_design"
