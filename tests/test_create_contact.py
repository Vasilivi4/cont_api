import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from shema_api.fun.crud import (
    create_contact,
    get_contact_mod,
    update_contact,
    delete_contact,
)
from shema_api.mod.models import User_mod
from shema_api.app.schema import ContactCreate, ContactUpdate
from shema_api.data.base import Base


# Setup для тестирования базы данных
SQLALCHEMY_DATABASE_URL = (
    "sqlite:///:memory:"  # Используется временная SQLite база данных
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание всех таблиц
Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    """Фикстура для работы с базой данных."""
    db = SessionLocal()
    try:
        # Сбрасываем все таблицы перед каждым тестом
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        yield db
    finally:
        db.close()


@pytest.fixture
def mock_user(db):
    """Создание фиктивного пользователя для тестирования."""
    user = User_mod(
        email="test@example.com", hashed_password="testpassword", first_name="Test"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def contact_data():
    """Данные для создания контакта."""
    unique_email = f"contact_{uuid.uuid4().hex}@example.com"
    return ContactCreate(
        name="Test Contact",
        email=unique_email,
        birthday="1990-01-01",
        first_name="John",  # Добавлено поле first_name
        last_name="Doe",  # Добавлено поле last_name
    )


def test_create_contact(db, mock_user, contact_data):
    """Тест для создания контакта."""
    contact_data = contact_data.model_copy(
        update={"owner_id": mock_user.id}
    )  # Добавляем owner_id
    contact = create_contact(
        db, contact_data, owner_id=mock_user.id
    )  # Передаем owner_id
    assert contact.first_name == contact_data.first_name  # Проверяем first_name
    assert contact.last_name == contact_data.last_name  # Проверяем last_name
    assert contact.email == contact_data.email
    assert contact.owner_id == mock_user.id  # Проверяем, что владелец правильный


def test_create_contact_duplicate_email(db, mock_user, contact_data):
    """Тест для проверки дублирующегося email."""
    # Создаем контакт с уникальным email
    create_contact(db, contact_data, owner_id=mock_user.id)

    # Пытаемся создать контакт с таким же email - должно вызвать IntegrityError
    with pytest.raises(IntegrityError):
        create_contact(db, contact_data, owner_id=mock_user.id)


def test_get_contacts(db, mock_user):
    """Тест для получения всех контактов пользователя."""
    contact = create_contact(
        db,
        ContactCreate(
            name="Another Contact",
            email="another@example.com",
            birthday="1991-01-01",
            first_name="Jane",  # Добавлено
            last_name="Smith",  # Добавлено
        ),
        owner_id=mock_user.id,
    )  # Устанавливаем владельца контакта
    contacts = get_contact_mod(db, mock_user)
    assert len(contacts) == 1
    assert contacts[0].first_name == "Jane"  # Проверяем first_name
    assert contacts[0].last_name == "Smith"  # Проверяем last_name


def test_update_contact(db, mock_user):
    """Тест для обновления контакта."""
    contact = create_contact(
        db,
        ContactCreate(
            name="Old Name",
            email="old@example.com",
            birthday="1990-01-01",
            first_name="Alice",  # Добавлено
            last_name="Brown",  # Добавлено
        ),
        owner_id=mock_user.id,
    )  # Устанавливаем владельца контакта

    updated_data = ContactUpdate(
        name="New Name",
        first_name="UpdatedFirstName",  # Обновляем first_name
        last_name="UpdatedLastName",  # Обновляем last_name
        email="updated@example.com",  # Обновляем email
    )
    updated_contact = update_contact(db, contact.id, updated_data)
    assert updated_contact.first_name == "UpdatedFirstName"  # Проверяем first_name
    assert updated_contact.last_name == "UpdatedLastName"  # Проверяем last_name
    assert updated_contact.email == "updated@example.com"  # Проверяем email


def test_delete_contact(db, mock_user):
    """Тест для удаления контакта."""
    contact = create_contact(
        db,
        ContactCreate(
            name="Contact to delete",
            email="delete@example.com",
            birthday="1990-01-01",
            first_name="Charlie",  # Добавлено
            last_name="Davis",  # Добавлено
        ),
        owner_id=mock_user.id,
    )  # Устанавливаем владельца контакта

    delete_contact(db, contact.id)
    contacts = get_contact_mod(db, mock_user)
    assert len(contacts) == 0
