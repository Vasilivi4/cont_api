import pytest
from sqlalchemy.orm import Session
from shema_api.data.base import get_db
from unittest.mock import patch

@pytest.fixture
def mock_database_url():
    """Мокаем DATABASE_URL для тестирования"""
    with patch.dict('os.environ', {'SQLALCHEMY_DATABASE_URL': 'sqlite:///:memory:'}):
        yield

@pytest.fixture
def db_session(mock_database_url):
    """Фикстура для предоставления сессии базы данных."""
    db = next(get_db())  # Получаем сессию через get_db()
    try:
        yield db
    finally:
        db.close()

def test_get_db(db_session):
    """Тест для функции get_db"""
    # Проверяем, что сессия создана
    assert db_session is not None
    assert isinstance(db_session, Session)