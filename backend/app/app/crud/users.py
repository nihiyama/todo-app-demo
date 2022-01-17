from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import verify_password, get_hashed_password, get_uuid


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    
    def get_by_email_address(self, db: Session, *, email_address: str) -> Optional[User]:
        try:
            return db.query(User).filter(User.email_address == email_address).first()
        except Exception as e:
            raise e
    
    def get_by_email_addresses(self, db: Session, *, email_addresses: List[str]) -> List[User]:
        try:
            return db.query(User).\
                filter(User.email_address.in_(email_addresses)).\
                order_by(User.id).\
                all()
        except Exception as e:
            raise e
    
    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[User]:
        try:
            return db.query(User).filter(User.uuid == uuid).first()
        except Exception as e:
            raise e

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        try:
            while True:
                uuid = get_uuid(length=32)
                user = self.get_by_uuid(db, uuid=uuid)
                if user is None:
                    break

            db_obj = User(
                email_address=obj_in.email_address,
                uuid=uuid,
                user_name=obj_in.user_name,
                hashed_password=get_hashed_password(obj_in.password),
                is_superuser=obj_in.is_superuser,
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
            
        except Exception as e:
            db.rollback()
            raise e
    
    def update(
        self,
        db: Session, 
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        try:
            if (password := update_data.get("password")) is not None:
                hashed_password = get_hashed_password(password)
                update_data["hashed_password"] = hashed_password
                update_data.pop("password")
            return super().update(db, db_obj=db_obj, obj_in=update_data)
        except Exception as e:
            db.rollback()
            raise e
    
    def authenticate(self, db: Session, *, email_address: str, password: str) -> Optional[User]:
        try:
            user = self.get_by_email_address(db, email_address=email_address)
            if user is None:
                return None
            if not verify_password(password, user.hashed_password):
                return None
            return user
        except Exception as e:
            raise e


user = CRUDUser(User)
