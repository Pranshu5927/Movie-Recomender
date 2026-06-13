from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Movie Recommender API is running"
    }


def test_signup_and_login():
    signup_payload = {
        "username": "ci_test_user",
        "email": "ci_test_user@example.com",
        "password": "TestPassword123"
    }

    signup_response = client.post("/auth/signup", json=signup_payload)
    assert signup_response.status_code == 200
    assert signup_response.json() == {"message": "User created successfully"}

    login_response = client.post("/auth/login", json={
        "email": signup_payload["email"],
        "password": signup_payload["password"]
    })
    assert login_response.status_code == 200

    body = login_response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_with_wrong_password_fails():
    response = client.post("/auth/login", json={
        "email": "ci_test_user@example.com",
        "password": "wrong-password"
    })

    assert response.status_code == 401


def test_login_with_unknown_email_fails():
    response = client.post("/auth/login", json={
        "email": "does-not-exist@example.com",
        "password": "whatever"
    })

    assert response.status_code == 401


def test_movies_endpoint_with_empty_db():
    response = client.get("/movies")

    assert response.status_code == 200
    assert response.json() == []
