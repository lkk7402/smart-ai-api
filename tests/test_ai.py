import pytest
from unittest.mock import MagicMock
from main import app
from ai.groq_client import get_groq_client


@pytest.fixture
def mock_groq():
    mock = MagicMock()
    mock.summarise.return_value = "This is a test summary."
    mock.chat.return_value = "Hello! How can I help?"
    mock.sentiment.return_value = {
        "sentiment": "positive",
        "score": 0.9,
        "explanation": "Very positive tone.",
    }
    app.dependency_overrides[get_groq_client] = lambda: mock
    yield mock
    app.dependency_overrides.pop(get_groq_client, None)


def test_summarise_success(client, auth_headers, mock_groq):
    resp = client.post(
        "/ai/summarise",
        json={"text": "FastAPI is a modern web framework for building APIs."},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["summary"] == "This is a test summary."
    mock_groq.summarise.assert_called_once()


def test_summarise_unauthenticated(client, mock_groq):
    resp = client.post("/ai/summarise", json={"text": "hello"})
    assert resp.status_code == 401


def test_chat_success(client, auth_headers, mock_groq):
    resp = client.post(
        "/ai/chat",
        json={"messages": [{"role": "user", "content": "Hi there"}]},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["reply"] == "Hello! How can I help?"


def test_chat_unauthenticated(client, mock_groq):
    resp = client.post(
        "/ai/chat",
        json={"messages": [{"role": "user", "content": "Hi"}]},
    )
    assert resp.status_code == 401


def test_sentiment_success(client, auth_headers, mock_groq):
    resp = client.post(
        "/ai/sentiment",
        json={"text": "I absolutely love this product!"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["sentiment"] == "positive"
    assert data["score"] == 0.9
    assert "explanation" in data


def test_sentiment_unauthenticated(client, mock_groq):
    resp = client.post("/ai/sentiment", json={"text": "test"})
    assert resp.status_code == 401
