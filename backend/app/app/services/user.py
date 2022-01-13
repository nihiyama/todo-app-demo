from typing import Optional
from pathlib import Path
import shutil

from fastapi import UploadFile, File
from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils.config import settings
from app.utils.mail import (
    create_signup_mail_content, create_signup_mail_subject,
    send_dummy_mail
)

avatar_dir = Path(settings.MEDIA_FILEPATH) / "avatar"

def create_user_and_send_mail(db: Session, * user_in: schemas.UserCreate, avatar: Optional[UploadFile]) -> None:
    user = crud.user.create(db, obj_in=user_in)
    user_name = user.user_name if user.user_name is not None else ""
    
    copy_avatar(uuid=user.uuid, avatar=avatar)
    mail_content = create_signup_mail_content(user_name=user_name, url=settings.SERVICE_URL)
    mail_subject = create_signup_mail_subject()
    send_dummy_mail(
        content=mail_content,
        subject=mail_subject,
        email_to=[user.email_address]
    )


def copy_avatar(uuid: str, avatar: Optional[UploadFile]) -> None:
    if avatar is not None:
        filename = Path(avatar.filename)
        suffix = filename.suffix
        with open((avatar_dir / uuid).with_suffix(suffix), "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
    else:
        default = avatar_dir / "user.png"
        suffix = default.suffix
        shutil.copy(default, (avatar_dir / uuid).with_suffix(suffix))

