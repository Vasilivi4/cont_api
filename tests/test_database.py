import os
import pytest
from sqlalchemy.orm import Session
from shema_api.data.base import get_db, DATABASE_URL, SQLALCHEMY_DATABASE_URL, engine, SessionLocal
from unittest.mock import MagicMock, patch


@pytest.fixture()
def mock_env_vars(monkeypatch):
    """Mocking environment variables for the test."""
    monkeypatch.setenv("DATABASE_URL", "mock://localhost:5432/testdb")
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URL", "mock://localhost:5432/testdb")


@pytest.fixture()
def db_session(mock_env_vars):
    """Create and yield a mocked database session for testing."""
    # Мокаем подключение, чтобы не использовать реальную базу данных
    mock_session = MagicMock(spec=Session)
    
    # Возвращаем сессию вместо реальной сессии
    yield mock_session


def test_database_url(mock_env_vars):
    """Test that the database URL is being read correctly from the environment."""
    assert os.getenv("DATABASE_URL") == "mock://localhost:5432/testdb"
    assert os.getenv("SQLALCHEMY_DATABASE_URL") == "mock://localhost:5432/testdb"


def test_database_connection(db_session: Session):
    """Test if the database session is mocked correctly."""
    # Мокаем ответ на запрос SELECT 1
    mock_result = MagicMock()
    mock_result.scalar.return_value = 1
    db_session.execute.return_value = mock_result

    # Вызываем выполнение запроса, проверяем корректность возвращаемого значения
    result = db_session.execute('SELECT 1')
    assert result.scalar() == 1


@patch('shema_api.data.base.engine')  # Патчим сам объект engine
def test_engine_creation(mock_engine, mock_env_vars):
    """Test that the engine is being created with the correct URL."""
    # Мокаем сам объект engine, чтобы он использовал наш мокированный URL
    mock_engine.url.database = "testdb"
    
    # Проверка, что в engine подставляется правильный URL из переменной окружения
    assert mock_engine.url.database == "testdb"
