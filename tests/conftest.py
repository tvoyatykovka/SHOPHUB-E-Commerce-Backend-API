import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Тестовая база данных (SQLite в памяти)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    # Создаём таблицы перед каждым тестом
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Удаляем после теста
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_token(client):
    # Регистрируем пользователя
    client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "123456"
    })
    # Логинимся и получаем токен
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "123456"
    })
    return response.json()["access_token"]