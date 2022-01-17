from typing import Any, Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, selectinload

from app.crud.base import CRUDBase
from app.crud.users import user
from app.models.todo_board import TodoBoard
from app.schemas.todo_board import TodoBoardCreate, TodoBoardUpdate
from app.models.user import User
from app.models.user_todo_board_association import UserTodoBoardAssociation

class CRUDBoard(CRUDBase[TodoBoard, TodoBoardCreate, TodoBoardUpdate]):
    
    def get_all_by_current_user(
        self,
        db: Session,
        *,
        current_user: User
    ) -> List[TodoBoard]:
        try:
            return db.query(TodoBoard).\
                    join(TodoBoard.users).\
                    filter(UserTodoBoardAssociation.user_id == current_user.id).\
                    order_by(TodoBoard.id).\
                    all()
        except Exception as e:
            raise e
    
    def get_by_uuids_and_current_user(
        self,
        db: Session,
        *,
        current_user: User,
        todo_board_uuids: Optional[List[str]] = None
    ) -> List[TodoBoard]:
        try:
            if todo_board_uuids is None:
                return self.get_all_by_current_user(db, current_user=current_user)
            else:
                return db.query(TodoBoard).\
                        join(TodoBoard.users).\
                        filter(
                            UserTodoBoardAssociation.user_id == current_user.id,
                            TodoBoard.uuid.in_(todo_board_uuids)
                        ).\
                        order_by(TodoBoard.id).\
                        all()
        except Exception as e:
            raise e

    def get_by_uuid_and_current_user(
        self,
        db: Session,
        *,
        current_user: User,
        todo_board_uuid: str
    ) -> Optional[TodoBoard]:
        try:
            return db.query(TodoBoard).\
                        filter(TodoBoard.uuid == todo_board_uuid).\
                        join(TodoBoard.users).\
                        filter(
                            UserTodoBoardAssociation.user_id == current_user.id,
                        ).\
                        options(selectinload(TodoBoard.todo_lists)).\
                        first()
        except Exception as e:
            raise e
    
    def get_by_uuid_and_current_owner(
        self,
        db: Session,
        *,
        current_user: User,
        todo_board_uuid: str
    ) -> Optional[TodoBoard]:
        try:
            return db.query(TodoBoard).\
                        filter(TodoBoard.uuid == todo_board_uuid).\
                        join(TodoBoard.users).\
                        filter(
                            UserTodoBoardAssociation.user_id == current_user.id,
                            UserTodoBoardAssociation.is_owner is True
                        ).\
                        options(selectinload(TodoBoard.todo_lists)).\
                        first()
        except Exception as e:
            raise e
    
    def create_by_current_user(self, db: Session, *, obj_in: TodoBoardCreate, current_user: User) -> TodoBoard:
        try:
            obj_in_data = jsonable_encoder(obj_in, by_alias=False)
            db_obj = self.model(**obj_in_data)
            a_obj = UserTodoBoardAssociation(
                user_id=current_user.id,
                is_owner=True
            )
            db_obj.users.append(a_obj)
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
        db_obj: TodoBoard,
        obj_in: Union[TodoBoardUpdate, Dict[str, Any]]
    ) -> TodoBoard:
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            a_users: List[UserTodoBoardAssociation] = db_obj.users
            a_users_owner_map = {a_user_.user_id: a_user_.is_owner for a_user_ in a_users}
            if (useable_user_email_addresses := update_data.get("useable_user_email_addresses")) is not None:
                users = user.get_by_email_addresses(db, email_addresses=useable_user_email_addresses)
                useable_user_is_owners = update_data.get("useable_user_is_owners")
                a_objs: List[UserTodoBoardAssociation] = []
                for user_ in users:
                    if useable_user_is_owners is None:
                        is_owner = v if (v := a_users_owner_map.get(user_.id)) is not None else False
                        a_objs.append(
                            UserTodoBoardAssociation(
                                user_id = user_.id,
                                is_owner = is_owner
                            )
                        )
                    elif useable_user_is_owners is not None and user_.email_address in useable_user_is_owners:
                        a_objs.append(
                            UserTodoBoardAssociation(
                                user_id = user_.id,
                                is_owner = True
                            )
                        )
                    else:
                        a_objs.append(
                            UserTodoBoardAssociation(
                                user_id = user_.id,
                                is_owner = False
                            )
                        )
                db_obj.users = a_objs
                update_data.pop("useable_user_email_addresses")

            elif (useable_user_is_owners := update_data.get("useable_user_is_owners")) is not None:    
                users = user.get_by_email_addresses(db, email_addresses=useable_user_is_owners)
                useable_users_owner_map = {e.id: e.email_address for e in users}
                a_objs: List[UserTodoBoardAssociation] = []
                for user_id in a_users_owner_map:
                    if user_id in useable_users_owner_map:
                        a_objs.append(
                            UserTodoBoardAssociation(
                                user_id = user_id,
                                is_owner = True
                            )
                        )
                    else:
                        a_objs.append(
                            UserTodoBoardAssociation(
                                user_id = user_id,
                                is_owner = False
                            )
                        )
                update_data.pop("useable_user_is_owners")

            return super().update(db, db_obj=db_obj, obj_in=update_data)

        except Exception as e:
            db.rollback()
            raise e

    def update_list_order(self, db: Session, *, db_obj: TodoBoard, list_order: str) -> TodoBoard:
        update_data = {
            "list_order": list_order
        }
        return super().update(db, db_obj=db_obj, obj_in=update_data)

todo_board = CRUDBoard(TodoBoard)
