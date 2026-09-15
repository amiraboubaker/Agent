from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["service"] == "mobile-application-agent"


def test_chat_works_without_provider() -> None:
    response = client.post("/api/chat", json={"message": "Plan an Expo app with offline storage"})
    assert response.status_code == 200
    assert response.json()["task_type"] == "architecture"
    assert response.json()["answer"]
