from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"


def test_chat_endpoint_creates_conversation(monkeypatch) -> None:
    async def fake_answer(self, message, task_type, history):
        return "Mocked AI architecture guidance"

    monkeypatch.setattr("app.api.routes.LLMService.answer", fake_answer)
    response = client.post("/api/chat", json={"message": "Design a RAG pipeline with embeddings"})
    assert response.status_code == 200
    body = response.json()
    assert body["task_type"] == "rag"
    assert body["conversation_id"] > 0
    assert body["answer"]


def test_chat_validation_rejects_empty_message() -> None:
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 422


def test_chat_rejects_unknown_conversation() -> None:
    response = client.post("/api/chat", json={"message": "Continue", "conversation_id": 999999})
    assert response.status_code == 404


def test_chat_rate_limit_returns_429(monkeypatch) -> None:
    from app.api.routes import rate_limiter

    monkeypatch.setattr(rate_limiter, "allow", lambda *args, **kwargs: False)
    response = client.post("/api/chat", json={"message": "This should be limited"})
    assert response.status_code == 429
