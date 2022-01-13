

from typing import Generator, List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models
from app.utils import security
from app.utils.config import settings
from app.db.database import SessionLocal


def get_db() -> Generator:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), 
    Authorize: security.CookieAuthJwt = Depends()
) -> models.User:
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credential"
        )
    subject = Authorize.get_jwt_subject()
    raw_jwt = Authorize.get_raw_jwt()
    user = None
    if raw_jwt["user_type"] == "user":
        user = crud.user.get_by_uuid(db, uuid=subject)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the user or API client cannot access"
        )
    return user

def get_current_superuser(current_user: models.User = Depends(get_current_user)) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the resource"
        )
    return current_user
