"""Module providing a function printing python version."""

import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from dotenv import load_dotenv
from shema_api.app.schema import UserResponse, UserCreate, Token
from shema_api.fun.dependencies import get_current_user
from shema_api.fun.crud import (
    create_user_with_avatar,
    get_user_by_email,
    create_user,
    update_token,
)
from shema_api.data.base import get_db
from shema_api.fun.utils import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_password_mod,
)
from shema_api.mod.models import User_mod


load_dotenv(dotenv_path=".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Function register_user printing python version."""
    try:
        db_user = get_user_by_email(db, email=user.email)
        print(f"Checking for existing user: {db_user}")
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

        new_user = create_user(db, user)
        print(f"New user created: {new_user}")
        return new_user
    except Exception as e:
        print(f"Error during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/login", response_model=Token, tags=["auth"])
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Function login printing python version."""
    user = db.query(User_mod).filter(User_mod.email == body.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not verify_password_mod(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    await update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/create-users/", tags=["auth"])
async def create_users(body: UserCreate, db: Session = Depends(get_db)):
    """Function create_users printing python version."""
    new_user = create_user_with_avatar(body, db)
    return {"message": "User created successfully", "user": new_user}


@router.post("/token", response_model=Token, tags=["auth"])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Function login_for_access_token printing python version."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/refresh-token", tags=["auth"])
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    """Function refresh_access_token printing python version."""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    new_access_token = create_access_token(data={"sub": user.email})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get("/protected-route", tags=["auth"])
def protected_route(current_user: User_mod = Depends(get_current_user)):
    """Function protected_route printing python version."""
    return {"message": "You are authenticated", "user": current_user.email}
