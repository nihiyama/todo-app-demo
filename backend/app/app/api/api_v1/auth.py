from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps
from app.utils import security
from app.utils.config import settings


router = APIRouter()


@router.post("/login")
def login(
    db: Session = Depends(deps.get_db),
    Authorize: security.CookieAuthJwt = Depends(),
    *,
    auth_in: schemas.UserAuth
) -> Any:
    user = crud.user.authenticate(
        db,
        email_address=auth_in.email_address,
        password=auth_in.password
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email address or password"
        )
    user_claims = {"user_type": "user"}
    access_token = Authorize.create_access_token(subject=user.uuid, user_claims=user_claims)
    refresh_token = Authorize.create_refresh_token(subject=user.uuid, user_claims=user_claims)

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return {
        "detail": "Successfully login.",
        "expiresIn": timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }


@router.post("/refresh")
def refresh(
    Authorize: security.CookieAuthJwt = Depends()
) -> Any:
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    raw_jwt = Authorize.get_jwt_subject()
    user_claims = {"user_type": raw_jwt["user_type"]}
    new_access_token = Authorize.create_access_token(subject=current_user, user_claims=user_claims)
    new_refresh_token = Authorize.create_refresh_token(subject=current_user, user_claims=user_claims)
    
    Authorize.set_access_cookies(new_access_token)
    Authorize.set_refresh_cookies(new_refresh_token)
    
    return {
        "detail": "Token refresh was completed",
        "expiresIn": timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }


@router.post("/logout")
def logout(
    Authorize: security.CookieAuthJwt = Depends()
) -> Any:
    current_user = Authorize.get_jwt_subject()
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    
    return {
        "detail": "Successfully logout"
    }