from typing import Any, List, Optional

from fastapi import (
    APIRouter, Depends, HTTPException, status,
)
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.post("/todo-list", response_model=schemas.TodoBoard)
def move_todo_list(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    move_in: schemas.TodoListMove
) -> Any:
    todo_board = crud.todo_board.get_by_uuid_and_current_owner(
        db,
        current_user=current_user,
        todo_board_uuid=move_in.todo_board_uuid
    )
    if todo_board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the todo board"
        )
    todo_board = crud.todo_board.update_list_order(
        db,
        db_obj=todo_board,
        list_order=move_in.new_list_order
    )
    return todo_board


@router.post("/todo-card/{id}", response_model=List[schemas.TodoList])
def move_todo_card(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    id: int,
    move_in: schemas.TodoCardMove
) -> Any:
    if move_in.todo_list_id_with_after is None \
            or move_in.todo_list_id_with_before == move_in.todo_list_id_with_after:
        todo_list_with_before = crud.todo_list.get_by_id_and_current_user(
            db,
            current_user=current_user,
            todo_list_id=move_in.todo_list_id_with_before
        )
        if todo_list_with_before is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found the todo list"
            )
        todo_card = crud.todo_card.get_by_id_and_current_user(
            db,
            current_user=current_user,
            todo_card_id=id
        )
        if todo_card is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found the todo card"
            )
        todo_list_with_before = crud.todo_list.update_card_order(
            db,
            db_obj=todo_list_with_before,
            card_order=move_in.card_order_with_before
        )
        return [todo_list_with_before]
    else:
        todo_list_with_before = crud.todo_list.get_by_id_and_current_user(
            db,
            current_user=current_user,
            todo_list_id=move_in.todo_list_id_with_before
        )
        if todo_list_with_before is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found the todo list with before"
            )
        todo_list_with_after = crud.todo_list.get_by_id_and_current_user(
            db,
            current_user=current_user,
            todo_list_id=move_in.todo_list_id_with_after
        )
        if todo_list_with_after is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found the todo list with after"
            )
        todo_card = crud.todo_card.get_by_id_and_current_user(
            db,
            current_user=current_user,
            todo_card_id=id
        )
        if todo_card is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found the todo card"
            )
        todo_card = crud.todo_card.update(
            db,
            db_obj=todo_card,
            obj_in=schemas.TodoCardUpdate(
                todo_list_id=move_in.todo_list_id_with_after
            )
        )
        todo_list_with_before = crud.todo_list.get_by_id_and_current_user(
            db,
            current_user=current_user,
            todo_list_id=move_in.todo_list_id_with_before
        )
        todo_list_with_before = crud.todo_list.update_card_order(
            db,
            db_obj=todo_list_with_before,
            card_order=move_in.card_order_with_before
        )
        todo_list_with_after = crud.todo_list.get_by_id_and_current_user(
            db,
            current_user=current_user,
            todo_list_id=move_in.todo_list_id_with_after
        )
        todo_list_with_after = crud.todo_list.update_card_order(
            db,
            db_obj=todo_list_with_after,
            card_order=move_in.card_order_with_after,
        )
        return [todo_list_with_before, todo_list_with_after]    
