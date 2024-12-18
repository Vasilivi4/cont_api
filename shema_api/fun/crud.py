"""Module providing a function printing python version."""

import os
import bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt
from libgravatar import Gravatar
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from shema_api.mod.models import Contact_mod, User_mod, User
from shema_api.app.schema import ContactCreate, ContactUpdate, UserCreate


load_dotenv(dotenv_path=".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
try:
    hashed_password = pwd_context.hash("testpassword")
    print(f"Hashed password: {hashed_password}")
except Exception as e:
    print(f"Password hashing failed: {e}")


def get_contact_mod(db: Session, current_user: User_mod):
    """Function create_contact printing python version."""
    return db.query(Contact_mod).filter(Contact_mod.owner_id == current_user.id).all()


def get_contact_by_id(db: Session, contact_id: int):
    """Function create_contact printing python version."""
    return db.query(Contact_mod).filter(Contact_mod.id == contact_id).first()


def create_contact(db: Session, contact: ContactCreate, owner_id: int):
    """Функция для создания контакта с указанием владельца."""
    db_contact = Contact_mod(**contact.model_dump(), owner_id=owner_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact



def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    """Function update_contact printing python version."""
    db_contact = get_contact_by_id(db, contact_id)
    if db_contact:
        for key, value in contact.model_dump(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    """Function delete_contact printing python version."""
    db_contact = get_contact_by_id(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def get_upcoming_birthdays_mod(db: Session, days: int = 7, owner_id: int = None):
    """Function get_upcoming_birthdays_mod printing python version."""
    today = datetime.today().date()
    upcoming_date = today + timedelta(days=days)
    query = db.query(Contact_mod).filter(
        Contact_mod.birthday >= today, Contact_mod.birthday <= upcoming_date
    )
    if owner_id:
        query = query.filter(Contact_mod.owner_id == owner_id)

    return query.all()


def get_user_by_email(db: Session, email: str):
    """Function get_user_by_email printing python version."""
    if not isinstance(db, Session):
        raise ValueError("Expected db to be a Session object")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"User with email {email} not found.")
    return user


def create_user(db: Session, user: UserCreate) -> User_mod:
    """Function create_user printing python version."""
    print("Creating user...")
    print(f"User data: {user}")
    try:
        hashed_password = pwd_context.hash(user.password)
        print(f"Hashed password: {hashed_password}")

        db_user = User_mod(
            email=user.email,
            hashed_password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        print(f"Creating user with email: {db_user.email}")

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        print(f"User created successfully: {db_user}")
        return db_user

    except Exception as e:
        db.rollback()
        print(f"Failed to create user: {e}")
        raise Exception("Failed to create user")


def create_user_with_avatar(body: UserCreate, db: Session) -> User_mod:
    """Function create_user_with_avatar printing python version."""
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)

    hashed_password = bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt())

    hashed_password_str = hashed_password.decode("utf-8")

    new_user = User_mod(
        first_name=body.first_name,
        email=body.email,
        hashed_password=hashed_password_str,
        avatar=avatar,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


async def update_token(user: User_mod, token: str | None, db: Session) -> None:
    """Function update_token printing python version."""
    user.refresh_token = token
    db.commit()


def generate_email_token(email: str) -> str:
    """Function generate_email_token printing python version."""
    payload = {"sub": email}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
