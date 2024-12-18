from datetime import datetime, timedelta
from typing import Optional
import pytest
from unittest.mock import patch, MagicMock
from jose import JWTError, jwt
from fastapi import HTTPException
from shema_api.fun.utils import (
    hash_password,
    verify_password_mod,
    authenticate_user,
    send_email
)

SECRET_KEY = "testsecret"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[float] = None):
    """Создание access токена"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (timedelta(seconds=expires_delta) if expires_delta else timedelta(minutes=15))
    to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: Optional[float] = None):
    """Создание refresh токена"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (timedelta(seconds=expires_delta) if expires_delta else timedelta(days=7))
    to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_refresh_token(token: str):
    """Decode and validate a refresh token."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:  # Catch other JWT-related errors
        raise HTTPException(status_code=400, detail="Invalid token")

def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == data["sub"]
    assert "exp" in decoded
    assert "iat" in decoded

def test_create_refresh_token():
    data = {"sub": "test@example.com"}
    token = create_refresh_token(data)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == data["sub"]
    assert decoded["scope"] == "refresh_token"

def test_hash_password_and_verify():
    password = "securepassword"
    hashed = hash_password(password)
    assert verify_password_mod(password, hashed) is True
    assert verify_password_mod("wrongpassword", hashed) is False

@patch("sqlalchemy.orm.Session")
def test_authenticate_user(mock_session):
    mock_user = MagicMock()
    mock_user.hashed_password = hash_password("securepassword")
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user

    user = authenticate_user(mock_session, "username", "securepassword")
    assert user == mock_user

    user = authenticate_user(mock_session, "username", "wrongpassword")
    assert user is None

@patch("fastapi_mail.FastMail.send_message")
def test_send_email(mock_send_message):
    email = "test@example.com"
    send_email(email, "TestUser", "http://localhost")
    mock_send_message.assert_called_once()


def test_decode_refresh_token():
    # Setup
    valid_data = {"sub": "test@example.com"}
    token = jwt.encode(valid_data, SECRET_KEY, algorithm=ALGORITHM)
    
    # Test valid token
    assert decode_refresh_token(token) == valid_data["sub"]

    # Test expired token
    expired_token = jwt.encode(
        {**valid_data, "exp": datetime.utcnow() - timedelta(seconds=1)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    with pytest.raises(HTTPException) as exc_info:
        decode_refresh_token(expired_token)
    assert exc_info.value.status_code == 401
    assert "Token has expired" in str(exc_info.value.detail)

    # Test invalid token
    invalid_token = "invalid_token"
    with pytest.raises(HTTPException) as exc_info:
        decode_refresh_token(invalid_token)
    assert exc_info.value.status_code == 400
    assert "Invalid token" in str(exc_info.value.detail)
