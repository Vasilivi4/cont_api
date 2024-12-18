from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient
from main import app  # Ваш основной FastAPI приложение
from shema_api.mod.models import PasswordResetToken

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 1
    user.email = "testuser@example.com"
    return user

@pytest.fixture
def mock_db_session():
    """Мокаем сессию базы данных"""
    mock_db = MagicMock()
    return mock_db



def test_missing_token_in_password_reset(client):
    response = client.post(
        "/password-reset", json={"new_password": "new_password"}
    )

    assert response.status_code == 422  # Ошибка валидации данных
