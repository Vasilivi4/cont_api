"""Module providing a function printing python version."""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from shema_api.data.base import Base

class Contact_mod(Base):
    """Class Contact_mod representing a person"""
    __tablename__ = "contacts_mod"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True, nullable=False)
    last_name = Column(String(50), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone_number = Column(String(15), nullable=True)
    birthday = Column(Date, nullable=True)
    additional_info = Column(String(255), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now()) 
    owner_id = Column(Integer, ForeignKey("users_mod.id"))

    owner = relationship("User_mod", back_populates="contacts_mod")

class User_mod(Base):
    """Class User_mod representing a person"""
    __tablename__ = "users_mod"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now()) 
    avatar = Column(String(255), nullable=True)
    access_token = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    expired_at = Column(DateTime, default=datetime.utcnow)

    contacts_mod = relationship("Contact_mod", back_populates="owner")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")

    def __str__(self):
        return f"User(id={self.id}, username={self.first_name}, email={self.email}, is_active={self.is_active})"

class PasswordResetToken(Base):
    """Class PasswordResetToken representing a person"""
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users_mod.id'))
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    expired_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User_mod", back_populates="password_reset_tokens")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

