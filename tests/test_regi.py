from http import client
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from shema_api.data.base import get_db, Base

import pytest
from fastapi.testclient import TestClient
from main import app  # Импортируй приложение FastAPI

client = TestClient(app)  # Инициализируй TestClient с приложением

def test_register_user():
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
        },
    )
    print(response.status_code)
    print(response.json())  # Добавляем вывод содержимого ответа для диагностики
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


def test_login_user():
    response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "password123"},
    )
    print(response.status_code)
    print(response.json())  # Логирование содержимого ответа
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_protected_route():
    # Регистрация пользователя
    client.post(
        "/register",
        json={
            "email": "testprotected@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "ProtectedUser",
        },
    )
    # Вход в систему
    login_response = client.post(
        "/login",
        data={"username": "testprotected@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Проверка защищенного маршрута
    response = client.get(
        "/protected-route", headers={"Authorization": f"Bearer {token}"}
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200

# Создаем тестовую базу данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы для тестовой базы
Base.metadata.create_all(bind=engine)

# Фикстура для тестовой сессии
@pytest.fixture(scope="function")
def test_db():
    # Создаем новую сессию для каждого теста
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Переопределяем зависимость get_db на использование тестовой базы
@pytest.fixture(scope="module", autouse=True)
def override_get_db():
    def _get_test_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = _get_test_db


# Тесты
def test_registers_user(db_session):
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


def test_logins_user(db_session):
    response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_protecteds_route(db_session):
    # Логинимся для получения токена
    login_response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    # Используем токен для доступа к защищенному маршруту
    response = client.get(
        "/protected-route",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "You are authenticated"


def test_refresh_token(db_session):
    # Логинимся для получения токенов
    login_response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "password123"},
    )
    refresh_token = login_response.json()["refresh_token"]

    # Обновляем токен доступа
    response = client.post(
        "/refresh-token",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_invalid_credentials(db_session):
    response = client.post(
        "/login",
        data={"username": "wrong@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email"


def test_protected_route_with_invalid_token(db_session):
    response = client.get(
        "/protected-route",
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
