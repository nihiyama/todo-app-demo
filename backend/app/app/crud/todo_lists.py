from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, selectinload

from app.crud.todo_boards import todo_board
from app.crud.base import CRUDBase
from app.models.todo_list import TodoList
from app.models.todo_card import TodoCard
from app.models.user_todo_board_association import UserTodoBoardAssociation
from app.schemas.todo_list import TodoListCreate, TodoListUpdate
from app.models.user import User
from app.models.todo_board import TodoBoard
from app.services.todo import num_regex_p


class CRUDList(CRUDBase[TodoList, TodoListCreate, TodoListUpdate]):
    
    def get_all_by_current_user(
        self,
        db: Session,
        *,
        current_user: User,
        todo_board_uuids: Optional[List[str]] = None,
    ) -> List[TodoList]:
        try:
            todo_boards: List[TodoBoard] = todo_board.\
                                get_by_uuids_and_current_user(
                                    db,
                                    current_user=current_user,
                                    todo_board_uuids=todo_board_uuids
                                )
            todo_board_ids: List[int] = [e.id for e in todo_boards]
            return db.query(TodoList).\
                    filter(TodoList.todo_board_id.in_(todo_board_ids)).\
                    order_by(TodoList.todo_board_id, TodoList.id).\
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
    ) -> List[TodoList]:
        try:
            if todo_list_ids is None:
                return self.get_all_by_current_user(db, current_user=current_user, todo_board_uuids=todo_board_uuids)
            else:
                todo_boards: List[TodoBoard] = todo_board.\
                                get_by_uuids_and_current_user(
                                    db,
                                    current_user=current_user,
                                    todo_board_uuids=todo_board_uuids
                                )
                todo_board_ids: List[int] = [e.id for e in todo_boards]
                return db.query(TodoList).\
                        filter(TodoList.todo_board_id.in_(todo_board_ids), TodoList.id.in_(todo_list_ids)).\
                        order_by(TodoList.todo_board_id, TodoList.id).\
                        all()
        except Exception as e:
            raise e

    def get_by_id_and_current_user(
        self,
        db: Session,
        *,
        current_user: User,
        todo_list_id: int,
        is_order: bool = False
    ) -> Optional[TodoList]:
        try:
            todo_list_: Optional[TodoList] =  db.query(TodoList).\
                        filter(TodoList.id == todo_list_id).\
                        join(TodoList.todo_board).\
                        join(TodoBoard.users).\
                        filter(
                            UserTodoBoardAssociation.user_id == current_user.id
                        ).\
                        options(selectinload(TodoList.todo_cards).selectinload(TodoCard.assignees)).\
                        first()
            if todo_list_ is None:
                return todo_list_
            if is_order:
                # create order by dict to sort
                card_order = {
                    int(e): i
                    for i, e in enumerate(todo_list_.card_order.split(","))
                    if num_regex_p.match(e)
                }
                todo_cards: List[TodoCard] = todo_list_.todo_cards
                # if the card not exist in card_order but list exist in todo_cards, put the card first.
                todo_list_.todo_cards = sorted(todo_cards, key=lambda x: v if (v := card_order.get(x.id)) is not None else -1)
                return todo_list_
            else:
                return todo_list_
            
        except Exception as e:
            raise e
    
    def create_in_todo_board(
        self,
        db: Session,
        *,
        obj_in: TodoListCreate,
        todo_board_db_obj: TodoBoard
    ) -> TodoList:
        try:
            obj_in_data = jsonable_encoder(obj_in, by_alias=False)
            obj_in_data.pop("todo_board_uuid")
            db_obj = TodoList(
                todo_board_id = todo_board_db_obj.id,
                card_order="",
                **obj_in_data
            )
            db.add(db_obj)
            db.commit()
            list_order = todo_board_db_obj.list_order
            if list_order is None or list_order == "":
                todo_board.update_list_order(
                    db,
                    db_obj=todo_board_db_obj,
                    list_order=f"{db_obj.id}"
                )
            else:
                todo_board.update_list_order(
                    db,
                    db_obj=todo_board_db_obj,
                    list_order=f"{list_order},{db_obj.id}"
                )
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise e
    
    def update_card_order(self, db: Session, *, db_obj: TodoList, card_order: str) -> TodoList:
        update_data = {
            "card_order": card_order
        }
        print(jsonable_encoder(db_obj))
        return super().update(db, db_obj=db_obj, obj_in=update_data)

todo_list = CRUDList(TodoList)
