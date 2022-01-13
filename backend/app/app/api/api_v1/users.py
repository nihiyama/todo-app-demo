from typing import Any, List, Optional

from fastapi import (
    APIRouter, BackgroundTasks, Depends, HTTPException, status,
    UploadFile, File, Body
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils.mail import is_valid_email_address
from app.services.user import create_user_and_send_mail, copy_avatar

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_superuser)
) -> Any:
    users = crud.user.get_all(db)
    return users


@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.User
)
async def create_user(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_superuser),
    *,
    background_tasks: BackgroundTasks,
    email_address: str = Body(..., alias="emailAddress"),
    user_name: str = Body(..., alias="userName"),
    password: str = Body(...),
    is_superuser: Optional[bool] = Body(False),
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
        password=password,
        is_superuser=is_superuser
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



@router.get("/{uuid}", response_model=schemas.User)
def read_user_by_uuid(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_superuser),
    *,
    uuid: str,
) -> Any:
    user = crud.user.get_by_uuid(db, uuid=uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the User"
        )
    return user


@router.put("/{uuid}", response_model=schemas.User)
def update_user_by_uuid(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_superuser),
    *,
    uuid: str,
    user_in: schemas.UserUpdate,
    avatar: Optional[UploadFile] = File(None)
) -> Any:
    user = crud.user.get_by_uuid(db, uuid=uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the User"
        )
    if user_in.email_address is not None and user_in.email_address != user.email_address:
        user_ = crud.user.get_by_email_address(db, email_address=user_in.email_address)
        if user_ is not None:
            raise HTTPException(
                status=status.HTTP_404_NOT_FOUND,
                detail="The email address has been already used."
            )
    if user_in.password is not None and len(user_in.password) == 0:
        user_in.password = None
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    if avatar is not None:
        copy_avatar(uuid=user.uuid, avatar=avatar)
    return user


@router.delete("/{uuid}", response_model=schemas.User)
def update_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_superuser),
    *,
    uuid: str
) -> Any:
    user = crud.user.get_by_uuid(db, uuid=uuid)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the user"
        )
    user = crud.user.remove(db, user)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    return current_user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    me_in: schemas.UserMeUpdate,
    avatar: Optional[UploadFile] = File(None)
) -> Any:
    current_user_data = jsonable_encoder(current_user, by_alias=False)
    user_in = schemas.UserUpdate(**current_user_data)
    update_me_data = me_in.dict(exclude_unset=True)
    password: Optional[str] = update_me_data.get("password")
    new_password: Optional[str] = update_me_data.get("new_password")
    if new_password is not None and len(new_password) > 0:
        if password is not None \
                and crud.user.authenticate(db, email_address=current_user.email_address, password=password) \
                and password != new_password:
            user_in.password = new_password
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not change password."
            )
    if (email_address := update_me_data.get("email_address") is not None):
        user_in.email_address = email_address
    if (user_name := update_me_data.get("user_name")) is not None:
        user_in.user_name = user_name
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    if avatar is not None:
        copy_avatar(uuid=user.uuid, avatar=avatar)
    return user


@router.delete("/me", response_model=schemas.User)
def update_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    user = crud.user.remove(db, current_user)
    return user
