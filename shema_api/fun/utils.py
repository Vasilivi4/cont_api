"""Module providing a function printing python version."""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi_mail import FastMail, MessageSchema, MessageType
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import EmailStr
from sqlalchemy.orm import Session
from shema_api.fun.dependencies import auth_service
from shema_api.config import conf
from shema_api.mod.models import User_mod

load_dotenv(dotenv_path=".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[float] = None):
    """Function create_access_token printing python version."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
    encoded_access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_access_token



def create_refresh_token(data: dict, expires_delta: Optional[float] = None):
    """Function create_refresh_token printing python version."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
    encoded_refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_refresh_token



def verify_password_mod(plain_password: str, hashed_password: str) -> bool:
    """Function verify_password_mod printing python version."""
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        print(f"Comparing: {plain_password} with hashed: {hashed_password}")
        
        result = pwd_context.verify(plain_password, hashed_password)
        
        print(f"Password match: {result}")
        
        return result
    except Exception as e:
        raise Exception(f"Error verifying password: {e}")


def hash_password(password: str) -> str:
    """Function hash_password printing python version."""
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed = pwd_context.hash(password)
        return hashed
    except Exception as e:
        raise Exception(f"Error hashing password: {e}")
    
def hash_password_bcrypt(password: str) -> str:
    """Function hash_password_bcrypt printing python version."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def authenticate_user(db: Session, username: str, password: str):
    """Function authenticate_user printing python version."""
    user = db.query(User_mod).filter(User_mod.first_name == username).first()
    if user is None:
        logger.info(f"User with email {username} not found.")
        return None
    if not verify_password_mod(password, user.hashed_password):
        logger.info(f"Incorrect password for user {username}.")
        return None
    return user


def confirmed_email(email: str, db: Session):
    """Function confirmed_email printing python version."""
    user = db.query(User_mod).filter(User_mod.email == email).first()
    if user is None:
        return {"detail": "User not found"}
    user.confirmed = True
    user.is_active = True
    db.commit()
    return {"message": "Email confirmed"}



def send_email(email: EmailStr, username: str, host: str):
    """Function send_email printing python version."""
    try:
        token_verification = auth_service.create_email_token({"sub": email})

        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        fm.send_message(message, template_name="example_email.html")
    except ConnectionError as err:
        print(err)

async def send_reset_password_email(email: str, token: str):
    """Function send_reset_password_email printing python version."""
    host = "http://127.0.0.1:8000"
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        template_body={
            "username": email,
            "host": host,
            "token": token,
        },
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="reset_password_email.html")


def decode_refresh_token(token: str):
    """Function decode_refresh_token printing python version."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

    
def get_email_form_token(refresh_token: str):
    """Function get_email_form_token printing python version."""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload['scope'] == 'refresh_token':
            email = payload['sub']
            return email
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
