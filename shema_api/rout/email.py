"""Module providing a function printing python version."""

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlalchemy.orm import Session
from shema_api.app.schema import EmailSchema
from shema_api.config import conf
from shema_api.data.base import get_db
from shema_api.fun.utils import (
    confirmed_email,
    create_access_token,
    decode_refresh_token,
)
from shema_api.mod.models import User_mod

router = APIRouter()


@router.post("/send-email", tags=["email"])
async def send_in_background(
    background_tasks: BackgroundTasks, body: EmailSchema, db: Session = Depends(get_db)
):
    """Function send_in_background printing python version."""
    host = "http://127.0.0.1:8000"
    token = create_access_token({"sub": body.email})
    user = db.query(User_mod).filter(User_mod.email == body.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.access_token = token
    db.commit()
    db.refresh(user)
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={
            "username": "Num Shyrik muN",
            "host": host,
            "token": token,
        },
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    background_tasks.add_task(
        fm.send_message, message, template_name="example_email.html"
    )
    return {"message": "Email has been sent"}


@router.get("/shema_api/fun_class/confirmed_email/{token}", tags=["email"])
async def confirm_email(token: str, db: Session = Depends(get_db)):
    """Function confirm_email printing python version."""
    try:
        email = decode_refresh_token(token)

        response = confirmed_email(email, db)
        if "detail" in response:
            raise HTTPException(status_code=404, detail=response["detail"])

        return {"message": response["message"]}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
