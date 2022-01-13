from re import A
from typing import Any, Optional

from fastapi import (
    APIRouter, BackgroundTasks, Depends, HTTPException, status,
    UploadFile, File, Body
)
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.utils.mail import is_valid_email_address
from app.services.user import create_user_and_send_mail

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED
)
async def create_user(
    db: Session = Depends(deps.get_db),
    *,
    background_tasks: BackgroundTasks,
    email_address: str = Body(..., alias="emailAddress"),
    user_name: str = Body(..., alias="userName"),
    password: str = Body(...),
    avatar: Optional[UploadFile] = File(None)
) -> Any:
    if is_valid_email_address(email_address) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address is invalid"
        )
    user = crud.user.get_by_email_address(db, email_address=email_address)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user has already existed"
        )
    if avatar is not None:
        if "image" not in avatar.content_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="avatar mime type is must be image"
            )
    user_in = schemas.UserCreate(
        email_address=email_address,
        user_name=user_name,
        password=password
    )
    background_tasks.add_task(
        create_user_and_send_mail,
        db=db,
        user_in=user_in,
        avatar=avatar
    )
    return {
        "detail": "Accepted"
    }
