from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils.config import settings


def init_db(db: Session) -> None:
    user = crud.user.get_by_email_address(
        db,
        email_address=settings.FIRST_SUPERUSER
    )
    if user is not None:
        user_in = schemas.UserCreate(
            email_address=settings.FIRST_SUPERUSER,
            user_name="admin",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True
        )
        user = crud.user.create(db, obj_in=user_in)
