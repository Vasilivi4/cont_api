import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from shema_api.app.schema import UserCreate
from shema_api.data.base import Base  # Убедитесь, что путь корректный
from shema_api.mod.models import User_mod
from shema_api.fun.crud import create_user
from sqlalchemy.orm import Session

# Используем SQLite для тестов (в памяти)
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    # Настройка тестовой базы данных
    engine = create_engine(TEST_DATABASE_URL, echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session  # Передаем сессию для тестов
    finally:
        session.close()
        clear_mappers()  # Очистка мапперов SQLAlchemy
        Base.metadata.drop_all(bind=engine)  # Удаляем таблицы после теста



