"""Module providing a function printing python version."""

import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from shema_api.data.base import get_db
from shema_api.fun.dependencies import get_current_user
from shema_api.mod.models import User_mod
import logging

logging.basicConfig(level=logging.DEBUG)


router = APIRouter()

load_dotenv(dotenv_path=".env")

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)


@router.post("/upload-avatar/", tags=["email"])
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User_mod = Depends(get_current_user),
):
    """Function upload_avatar printing python version."""
    try:
        file_content = await file.read()

        max_file_size = 5 * 1024 * 1024
        if len(file_content) > max_file_size:
            raise HTTPException(
                status_code=400, detail="File is too large. Maximum size is 5MB."
            )

        allowed_extensions = ["jpg", "jpeg", "png"]
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only jpg, jpeg, and png are allowed.",
            )

        upload_response = cloudinary.uploader.upload(
            file_content, folder="avatars", resource_type="image"
        )

        avatar_url = upload_response.get("secure_url")

        current_user.avatar = avatar_url
        db.commit()
        db.refresh(current_user)

        return JSONResponse(
            content={"avatar_url": current_user.avatar}, status_code=200
        )

    except cloudinary.exceptions.Error as e:
        raise HTTPException(status_code=400, detail=f"Cloudinary error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"General error: {str(e)}")

@router.get("/some-secure-endpoint")
async def some_secure_endpoint():
    logging.debug("Endpoint reached")
    return {"message": "Success!"}