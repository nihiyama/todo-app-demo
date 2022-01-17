from typing import Any, Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.todo_lists import todo_list
from app.crud.users import user
from app.crud.base import CRUDBase
from app.models.todo_card import TodoCard
from app.models.todo_list import TodoList
from app.models.user_todo_board_association import UserTodoBoardAssociation
from app.schemas.todo_card import TodoCardCreate, TodoCardUpdate
from app.models.user import User
from app.models.todo_board import TodoBoard
from app.services.todo import num_regex_p


class CRUDCard(CRUDBase[TodoCard, TodoCardCreate, TodoCardUpdate]):
    
    def get_all_by_current_user(
        db: Session,
        *,
        current_user: User,
        todo_board_uuids: Optional[List[str]] = None,
        todo_list_ids: Optional[List[int]] = None,
    ) -> List[TodoCard]:
        try:
            todo_lists: List[TodoList] = todo_list.\
                                get_by_ids_and_current_user(
                                    db,
                                    current_user=current_user,
                                    todo_board_uuids=todo_board_uuids,
                                    todo_list_ids=todo_list_ids
                                )
            todo_list_ids: List[int] = [e.id for e in todo_lists]
            return db.query(TodoCard).\
                    filter(TodoCard.todo_list_id.in_(todo_list_ids)).\
                    order_by(TodoCard.todo_list_id, TodoCard.id).\
                    all()
        except Exception as e:
            raise e
        
    def get_by_ids_and_current_user(
        self,
        db: Session,
        *,
        current_user: User,
        todo_board_uuids: Optional[List[str]] = None,
        todo_list_ids: Optional[List[int]] = None,
        todo_card_ids: Optional[List[int]] = None,
    ) -> List[TodoCard]:
        try:
            if todo_card_ids is None:
                return self.get_all_by_current_user(
                                                db, 
                                                current_user=current_user,
                                                todo_board_uuids=todo_board_uuids,
                                                todo_list_ids=todo_list_ids
                                            )
            else:
                todo_lists: List[TodoList] = todo_list.\
                                get_by_ids_and_current_user(
                                    db,
                                    current_user=current_user,
                                    todo_board_uuids=todo_board_uuids,
                                    todo_list_ids=todo_list_ids
                                )
                todo_list_ids: List[int] = [e.id for e in todo_lists]
                return db.query(TodoCard).\
                        filter(TodoCard.todo_list_id.in_(todo_list_ids), TodoCard.id.in_(todo_card_ids)).\
                        order_by(TodoCard.todo_list_id, TodoCard.id).\
                        all()
        except Exception as e:
            raise e

    def get_by_list_id_and_current_user(
        self,
        db: Session,
        *,
        current_user: User,
        todo_list_id: Optional[List[int]] = None
    ) -> Optional[List[TodoCard]]:
        try:
            todo_list_: TodoList = todo_list.\
                                get_by_id_and_current_user(
                                    db,
                                    current_user=current_user,
                                    todo_list_id=todo_list_id
                                )
            if todo_list_ is None:
                return None
            else:
                # create order by dict to sort
                card_order = {
                    int(e): i
                    for i, e in enumerate(todo_list_.card_order.split(","))
                    if num_regex_p.match(e)
                }
                todo_cards: List[TodoCard] = todo_list_.todo_cards
                # if the card not exist in card_order but list exist in todo_cards, put the card first.
                return sorted(todo_cards, key=lambda x: v if (v := card_order.get(x)) is not None else -1)
        except Exception as e:
            raise e
    
    def get_by_id_and_current_user(
        self,
        db: Session,
        *,
        current_user: User,
        todo_card_id: int
    ) -> Optional[TodoCard]:
        try:
            return db.query(TodoCard).\
                        filter(TodoCard.id == todo_card_id).\
                        join(TodoCard.todo_list).\
                        join(TodoList.todo_board).\
                        join(TodoBoard.users).\
                        filter(
                            UserTodoBoardAssociation.user_id == current_user.id
                        ).\
                        first()
        except Exception as e:
            raise e
    
    def create_in_todo_list(
        self,
        db: Session,
        *,
        obj_in: TodoCardCreate,
        todo_list_db_obj: TodoList,
    ) -> TodoCard:
        try:
            obj_in_data: Dict[str, Any] = jsonable_encoder(obj_in, by_alias=False)
            obj_in_data.pop("assignees_email_address")
            db_obj = TodoCard(
                **obj_in_data
            )
            if (email_addresses := obj_in.assignees_email_address) is not None:
                assignees = user.get_by_email_addresses(db, email_addresses=email_addresses)
                db_obj.assignees = assignees
            db.add(db_obj)
            db.commit()
            if todo_list_db_obj.card_order is None:
                todo_list.update_card_order(
                    db,
                    db_obj=todo_list_db_obj,
                    list_order=f"{db_obj.id}"
                )
            else:
                todo_list.update_card_order(
                    db,
                    db_obj=todo_list_db_obj,
                    list_order=f"{db_obj.id},{todo_list_db_obj.card_order}"
                )
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise e
    
    def update(
        self,
        db: Session,
        *,
        db_obj: TodoCard,
        obj_in: Union[TodoCardUpdate, Dict[str, Any]]
    ) -> TodoCard:
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            if (email_addresses := update_data.get("assignees_email_address")) is not None:
                assignees = user.get_by_email_addresses(db, email_addresses=email_addresses)
                db_obj.assignees = assignees
            return super().update(db, db_obj=db_obj, obj_in=update_data)
        except Exception as e:
            db.rollback()
            raise e


todo_card = CRUDCard(TodoCard)
