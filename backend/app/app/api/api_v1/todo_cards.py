from typing import Any, List, Optional

from fastapi import (
    APIRouter, Depends, HTTPException, status,
    Query
)
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.TodoCard])
def read_todo_lists(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    todo_board_uuids: Optional[List[str]] = Query(None, alias="todoBoardUuids"),
    todo_list_ids: Optional[List[int]] = Query(None, alias="todoListIds"),
    todo_card_ids: Optional[List[int]] = Query(None, alias="todoCardIds"),
) -> Any:
    todo_cards = crud.todo_card.get_by_ids_and_current_user(
        db,
        current_user=current_user,
        todo_board_uuids=todo_board_uuids,
        todo_list_ids=todo_list_ids,
        todo_card_ids=todo_card_ids
    )
    return todo_cards


@router.post("/", response_model=schemas.TodoCard, status_code=status.HTTP_201_CREATED)
def create_todo_list(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    todo_card_in: schemas.TodoCardCreate
) -> Any:
    todo_list = crud.todo_list.get_by_id_and_current_user(
        db,
        current_user=current_user,
        todo_list_id=todo_card_in.todo_list_id
    )
    if todo_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the list"
        )
    todo_card = crud.todo_card.create_in_todo_list(
        db,
        obj_in=todo_card_in,
        todo_list_db_obj=todo_list
    )
    return todo_card


@router.get("/{id}", response_model=schemas.TodoCard)
def read_todo_card_by_id(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    id: int
) -> Any:
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
    return todo_card


@router.put("/{id}", response_model=schemas.TodoCard)
def update_todo_card_by_id(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    id: int,
    todo_card_in: schemas.TodoCardUpdate
) -> Any:
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
        obj_in=todo_card_in
    )
    return todo_card


@router.delete("/{id}", response_model=schemas.TodoCard)
def remove_todo_card_by_id(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    id: int
) -> Any:
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
    todo_card = crud.todo_card.remove(
        db,
        db_obj=todo_card
    )
    return todo_card
