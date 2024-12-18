import pytest
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from shema_api.data.base import Base
from shema_api.mod.models import User_mod, Contact_mod
from datetime import datetime

# Настройка базы данных для тестов
DATABASE_URL = "sqlite:///:memory:"  # Используем in-memory SQLite для тестов
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных и создания таблиц"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(setup_database):
    """Фикстура для создания сессии базы данных"""
    session = SessionLocal()
    yield session
    session.close()

def test_create_user(db_session):
    """Тест для создания пользователя"""
    new_user = User_mod(
        first_name="John",
        email="john.doe@example.com",
        hashed_password="hashedpassword123",
    )
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User_mod).filter_by(email="john.doe@example.com").first()
    assert user is not None
    assert user.first_name == "John"
    assert user.email == "john.doe@example.com"

def test_create_contact(db_session):
    """Тест для создания контакта"""
    new_user = User_mod(
        first_name="Jane",
        email="jane.doe@example.com",
        hashed_password="hashedpassword123",
    )
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User_mod).filter_by(email="jane.doe@example.com").first()
    new_contact = Contact_mod(
        first_name="John",
        last_name="Doe",
        email="john.contact@example.com",
        phone_number="123-456-7890",
        owner_id=user.id,
    )
    db_session.add(new_contact)
    db_session.commit()

    contact = db_session.query(Contact_mod).filter_by(email="john.contact@example.com").first()
    assert contact is not None
    assert contact.first_name == "John"
    assert contact.last_name == "Doe"

def test_user_contact_relationship(db_session):
    """Тест для проверки связи между пользователем и его контактами"""
    new_user = User_mod(
        first_name="Alice",
        email="alice.doe@example.com",
        hashed_password="hashedpassword123",
    )
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User_mod).filter_by(email="alice.doe@example.com").first()
    new_contact = Contact_mod(
        first_name="Bob",
        last_name="Smith",
        email="bob.contact@example.com",
        phone_number="987-654-3210",
        owner_id=user.id,
    )
    db_session.add(new_contact)
    db_session.commit()

    contacts = db_session.query(Contact_mod).filter_by(owner_id=user.id).all()
    assert len(contacts) == 1
    assert contacts[0].first_name == "Bob"

def test_delete_user(db_session):
    """Тест для удаления пользователя"""
    new_user = User_mod(
        first_name="Charlie",
        email="charlie.doe@example.com",
        hashed_password="hashedpassword123",
    )
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User_mod).filter_by(email="charlie.doe@example.com").first()
    db_session.delete(user)
    db_session.commit()

    deleted_user = db_session.query(User_mod).filter_by(email="charlie.doe@example.com").first()
    assert deleted_user is None

def test_unique_email_constraint(db_session):
    """Тест для проверки уникальности email"""
    new_user_1 = User_mod(
        first_name="Emma",
        email="emma.doe@example.com",
        hashed_password="hashedpassword123",
    )
    db_session.add(new_user_1)
    db_session.commit()

    new_user_2 = User_mod(
        first_name="Emily",
        email="emma.doe@example.com",
        hashed_password="hashedpassword456",
    )
    db_session.add(new_user_2)

    with pytest.raises(Exception):
        db_session.commit()
    db_session.rollback()

def test_birthday_filter(db_session):
    """Тест для фильтрации контактов по дате рождения"""
    new_user = User_mod(
        first_name="Liam",
        email="liam.doe@example.com",
        hashed_password="hashedpassword123",
    )
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User_mod).filter_by(email="liam.doe@example.com").first()
    contact = Contact_mod(
        first_name="Sophia",
        last_name="Brown",
        email="sophia.contact@example.com",
        birthday=datetime(1990, 5, 20),
        owner_id=user.id,
    )
    db_session.add(contact)
    db_session.commit()

    may_birthdays = db_session.query(Contact_mod).filter(func.strftime("%m", Contact_mod.birthday) == "05").all()
    assert len(may_birthdays) == 1