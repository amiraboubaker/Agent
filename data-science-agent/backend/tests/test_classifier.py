from app.agents.classifier import classify_task


def test_classifies_data_quality_request() -> None:
    assert classify_task("Find missing values and outliers") == "data_quality"


def test_classifies_modeling_request() -> None:
    assert classify_task("Build a regression model to predict sales") == "modeling"


def test_defaults_to_general_analysis() -> None:
    assert classify_task("Help me understand this dataset") == "general_analysis"
