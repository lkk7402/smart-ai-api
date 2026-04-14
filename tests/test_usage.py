from unittest.mock import MagicMock
from main import app
from ai.groq_client import get_groq_client


def _mock_groq():
    mock = MagicMock()
    mock.summarise.return_value = "summary"
    mock.sentiment.return_value = {
        "sentiment": "neutral",
        "score": 0.5,
        "explanation": "neutral",
    }
    app.dependency_overrides[get_groq_client] = lambda: mock
    return mock


def test_usage_empty(client, auth_headers):
    resp = client.get("/usage", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["total"] == 0
    assert resp.json()["breakdown"] == []


def test_usage_unauthenticated(client):
    resp = client.get("/usage")
    assert resp.status_code == 401


def test_usage_after_ai_calls(client, auth_headers):
    _mock_groq()

    client.post("/ai/summarise", json={"text": "test one"}, headers=auth_headers)
    client.post("/ai/summarise", json={"text": "test two"}, headers=auth_headers)
    client.post("/ai/sentiment", json={"text": "great!"}, headers=auth_headers)

    app.dependency_overrides.pop(get_groq_client, None)

    resp = client.get("/usage", headers=auth_headers)
    data = resp.json()
    assert data["total"] == 3

    breakdown = {item["endpoint"]: item["count"] for item in data["breakdown"]}
    assert breakdown["summarise"] == 2
    assert breakdown["sentiment"] == 1


def test_usage_isolated_per_user(client):
    # Two different users should see their own usage only
    _mock_groq()

    client.post("/auth/register", json={"email": "alice@example.com", "password": "pass"})
    r = client.post("/auth/login", data={"username": "alice@example.com", "password": "pass"})
    alice_headers = {"Authorization": f"Bearer {r.json()['access_token']}"}

    client.post("/auth/register", json={"email": "bob@example.com", "password": "pass"})
    r = client.post("/auth/login", data={"username": "bob@example.com", "password": "pass"})
    bob_headers = {"Authorization": f"Bearer {r.json()['access_token']}"}

    client.post("/ai/summarise", json={"text": "alice text"}, headers=alice_headers)

    app.dependency_overrides.pop(get_groq_client, None)

    alice_usage = client.get("/usage", headers=alice_headers).json()
    bob_usage = client.get("/usage", headers=bob_headers).json()

    assert alice_usage["total"] == 1
    assert bob_usage["total"] == 0
