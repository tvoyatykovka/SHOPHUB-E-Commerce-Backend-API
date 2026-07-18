import pytest
from app.main import client

def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "newuser@test.com",
        "username": "newuser",
        "password": "123456"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@test.com"
    assert "id" in response.json()

def test_register_duplicate_email(client):
    # Первый раз регистрируем
    client.post("/auth/register", json={
        "email": "duplicate@test.com",
        "username": "user1",
        "password": "123456"
    })
    # Второй раз с тем же email
    response = client.post("/auth/register", json={
        "email": "duplicate@test.com",
        "username": "user2",
        "password": "123456"
    })
    assert response.status_code == 400
    assert "already registered" in response.text

def test_register_duplicate_username(client):
    client.post("/auth/register", json={
        "email": "test1@test.com",
        "username": "sameuser",
        "password": "123456"
    })
    response = client.post("/auth/register", json={
        "email": "test2@test.com",
        "username": "sameuser",
        "password": "123456"
    })
    assert response.status_code == 400
    assert "already taken" in response.text

def test_login_success(client):
    client.post("/auth/register", json={
        "email": "login@test.com",
        "username": "loginuser",
        "password": "123456"
    })
    response = client.post("/auth/login", json={
        "email": "login@test.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "wrongpass@test.com",
        "username": "wronguser",
        "password": "123456"
    })
    response = client.post("/auth/login", json={
        "email": "wrongpass@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect" in response.text

def test_login_user_not_found(client):
    response = client.post("/auth/login", json={
        "email": "nonexistent@test.com",
        "password": "123456"
    })
    assert response.status_code == 401