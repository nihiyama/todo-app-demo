from typing import Any, List, Optional

from fastapi import (
    APIRouter, Depends, HTTPException, status,
    Query
)
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.TodoListBrevity])
def read_todo_lists(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    todo_board_uuids: Optional[List[str]] = Query(None, alias="todoBoardUuids"),
    todo_list_ids: Optional[List[int]] = Query(None, alias="todoListIds")
) -> Any:
    todo_lists = crud.todo_list.get_by_ids_and_current_user(
        db,
        current_user=current_user,
        todo_board_uuids=todo_board_uuids,
        todo_list_ids=todo_list_ids
    )
    return todo_lists


@router.post("/", response_model=schemas.TodoListBrevity, status_code=status.HTTP_201_CREATED)
def create_todo_list(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    todo_list_in: schemas.TodoListCreate
) -> Any:
    todo_board = crud.todo_board.get_by_uuid_and_current_owner(
        db,
        current_user=current_user,
        todo_board_uuid=todo_list_in.todo_board_uuid
    )
    if todo_board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the board or forbidden"
        )
    todo_list = crud.todo_list.create_in_todo_board(
        db,
        obj_in=todo_list_in,
        todo_board_db_obj=todo_board,
    )
    return todo_list


@router.get("/{id}", response_model=schemas.TodoList)
def read_todo_list_by_id(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    id: int
) -> Any:
    todo_list = crud.todo_list.get_by_id_and_current_user(
        db,
        current_user=current_user,
        todo_list_id=id
    ) 
    if todo_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the todo list"
        )
    return todo_list


@router.put("/{id}", response_model=schemas.TodoList)
def update_todo_list_by_id(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    id: int,
    todo_list_in: schemas.TodoListUpdate
) -> Any:
    todo_list = crud.todo_list.get_by_id_and_current_user(
        db,
        current_user=current_user,
        todo_list_id=id
    ) 
    if todo_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the todo list"
        )
    todo_list = crud.todo_list.update(
        db,
        db_obj=todo_list,
        obj_in=todo_list_in
    )
    return todo_list


@router.delete("/{id}", response_model=schemas.TodoList)
def remove_todo_list_by_id(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    id: int
) -> Any:
    todo_list = crud.todo_list.get_by_id_and_current_user(
        db,
        current_user=current_user,
        todo_list_id=id
    ) 
    if todo_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the todo list"
        )
    todo_list = crud.todo_list.remove(
        db,
        db_obj=todo_list
    )
    return todo_list
