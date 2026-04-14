def test_register_success(client):
    resp = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "secret123"},
    )
    assert resp.status_code == 201
    assert "access_token" in resp.json()
    assert resp.json()["token_type"] == "bearer"


def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "dup@example.com", "password": "pass"})
    resp = client.post("/auth/register", json={"email": "dup@example.com", "password": "pass"})
    assert resp.status_code == 400
    assert "already registered" in resp.json()["detail"]


def test_login_success(client):
    client.post("/auth/register", json={"email": "login@example.com", "password": "mypass"})
    resp = client.post("/auth/login", data={"username": "login@example.com", "password": "mypass"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "wp@example.com", "password": "correct"})
    resp = client.post("/auth/login", data={"username": "wp@example.com", "password": "wrong"})
    assert resp.status_code == 401


def test_login_unknown_email(client):
    resp = client.post("/auth/login", data={"username": "nobody@example.com", "password": "pass"})
    assert resp.status_code == 401
