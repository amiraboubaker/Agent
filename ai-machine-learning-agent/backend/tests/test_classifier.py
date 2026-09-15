from app.agents.classifier import classify_task


def test_classifies_rag_request() -> None:
    assert classify_task("Design a RAG pipeline with embeddings") == "rag"


def test_classifies_evaluation_request() -> None:
    assert classify_task("Evaluate accuracy and latency") == "evaluation"


def test_defaults_to_general_ai() -> None:
    assert classify_task("Help me think through this product") == "general_ai"
