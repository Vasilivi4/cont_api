"""Module providing a function printing python version."""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import date

class ContactBase(BaseModel):
    """Class ContactBase representing a person"""
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=15)
    birthday: Optional[date] = None
    additional_info: Optional[str] = None

class ContactCreate(ContactBase):
    """Class ContactCreate representing a person"""
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    birthday: Optional[date] = None

class ContactUpdate(ContactBase):
    """Class ContactUpdate representing a person"""
    pass

class ContactResponse(ContactBase):
    """Class ContactResponse representing a person"""
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None

    class Config:
        """Class ConfigContactResponse representing a person"""
        from_attributes = True

class UserCreate(BaseModel):
    """Class UserCreate representing a person"""
    email: EmailStr
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8, max_length=20)


class UserResponse(BaseModel):
    """Class UserResponse representing a person"""
    id: int = 1
    email: EmailStr
    first_name: str = Field(..., max_length=50)

class UserCreateResponse(BaseModel):
    """Class UserCreateResponse representing a person"""
    user: UserResponse
    detail: str

class PasswordResetRequest(BaseModel):
    """Class PasswordResetRequest representing a person"""
    token: str
    new_password: str

    class Config:
        """Class ConfigPasswordResetRequest representing a person"""
        from_attributes = True

class Token(BaseModel):
    """Class Token representing a person"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class Contact(BaseModel):
    """Class Contact representing a person"""
    id: int
    first_name: str = Field(..., max_length=50)
    phone_number: Optional[str] = Field(None, max_length=15)
    email: EmailStr

    class Config:
        """Class ConfigContact representing a person"""
        from_attributes = True

class EmailSchema(BaseModel):
    """Class EmailSchema representing a person"""
    email: EmailStr