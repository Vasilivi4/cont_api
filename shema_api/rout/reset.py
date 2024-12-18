"""Module providing a function printing python version."""

from datetime import datetime, timedelta
import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.background import BackgroundTasks
from pydantic import EmailStr
from sqlalchemy.orm import Session
from shema_api.app.schema import PasswordResetRequest
from shema_api.data.base import get_db
from shema_api.fun.utils import hash_password_bcrypt, send_reset_password_email
from shema_api.mod.models import User_mod, PasswordResetToken



router = APIRouter()


@router.post("/password-reset-request/")
def password_reset_request(
    email: EmailStr, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """Function password_reset_request printing python version."""
    user = db.query(User_mod).filter(User_mod.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = str(uuid.uuid4())
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    token_entry = PasswordResetToken(
        user_id=user.id, token=reset_token, expired_at=expiration_time
    )
    db.add(token_entry)
    db.commit()
    db.refresh(token_entry)

    background_tasks.add_task(send_reset_password_email, email, reset_token)

    return {"message": "Password reset token sent"}


@router.post("/password-reset")
async def password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """Function password_reset printing python version."""
    reset_token = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token == request.token)
        .first()
    )
    if not reset_token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    if reset_token.expired_at and reset_token.expired_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token has expired")

    user = db.query(User_mod).filter(User_mod.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = hash_password_bcrypt(request.new_password)

    user.hashed_password = hashed_password
    db.commit()

    db.delete(reset_token)
    db.commit()

    return {"message": "Password has been reset successfully"}


@router.get("/reset-password/{token}")
async def reset_password_form(token: str, db: Session = Depends(get_db)):
    """Function reset_password_form printing python version."""
    reset_token = (
        db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
    )
    if not reset_token:
        raise HTTPException(status_code=404, detail="Token not found or expired")

    if reset_token.expired_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token has expired")

    return {"message": "Token is valid. Please provide a new password.", "token": token}
