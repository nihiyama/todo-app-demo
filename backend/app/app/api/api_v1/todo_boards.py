from typing import Any, List, Optional

from fastapi import (
    APIRouter, Depends, HTTPException, status,
    Query
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.TodoBoardBrevity])
def read_todo_boards(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    todo_board_uuids: Optional[List[str]] = Query(None, alias="todoBoardUuids")
) -> Any:
    todo_boards = crud.todo_board.get_by_uuids_and_current_user(
        db,
        current_user=current_user,
        todo_board_uuids=todo_board_uuids
    )
    return todo_boards


@router.post("/", response_model=schemas.TodoBoardBrevity, status_code=status.HTTP_201_CREATED)
def create_todo_board(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    todo_board_in: schemas.TodoBoardCreate
) -> Any:
    todo_board = crud.todo_board.create_by_current_user(
        db,
        obj_in=todo_board_in,
        current_user=current_user
    )
    return todo_board


@router.get("/{uuid}", response_model=schemas.TodoBoard)
def read_todo_board_by_uuid(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    uuid: str
) -> Any:
    todo_board = crud.todo_board.get_by_uuid_and_current_user(
        db,
        current_user=current_user,
        todo_board_uuid=uuid,
        is_order=True
    )
    if todo_board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the todo board"
        )
    return todo_board


@router.put("/{uuid}", response_model=schemas.TodoBoard)
def update_todo_board_by_uuid(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    uuid: str,
    todo_board_in: schemas.TodoBoardUpdate
) -> Any:
    todo_board = crud.todo_board.get_by_uuid_and_current_owner(
        db,
        current_user=current_user,
        todo_board_uuid=uuid
    )
    if todo_board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the todo board"
        )
    todo_board = crud.todo_board.update(
        db,
        db_obj=todo_board,
        obj_in=todo_board_in
    )
    return todo_board


@router.delete("/{uuid}", response_model=schemas.TodoBoard)
def remove_todo_board_by_uuid(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    *,
    uuid: str
) -> Any:
    todo_board = crud.todo_board.get_by_uuid_and_current_owner(
        db,
        current_user=current_user,
        todo_board_uuid=uuid
    )
    if todo_board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the todo board"
        )
    todo_board = crud.todo_board.remove(
        db,
        db_obj=todo_board
    )
    return todo_board
