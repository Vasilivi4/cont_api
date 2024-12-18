"""Module providing a function printing python version."""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from shema_api.data.base import get_db
from shema_api.mod.models import Contact_mod, User_mod

load_dotenv(dotenv_path=".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """Function get_current_user printing python version."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["scope"] == "access_token":
            email = payload["sub"]
            if email is None:
                raise credentials_exception
        else:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user: User_mod = db.query(User_mod).filter(User_mod.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User_mod = Depends(get_current_user),
):
    """Function get_contact printing python version."""
    contact = (
        db.query(Contact_mod)
        .filter(Contact_mod.id == contact_id, Contact_mod.owner_id == current_user.id)
        .first()
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


class Auth:
    """Class Auth representing a person"""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/rout/auth/login")

    def __init__(self):
        if not self.SECRET_KEY or not self.ALGORITHM:
            raise ValueError(
                "SECRET_KEY and ALGORITHM must be set in environment variables"
            )

    def create_email_token(self, data: dict):
        """Function create_email_token printing python version."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "sub": data["sub"]})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token


auth_service = Auth()
