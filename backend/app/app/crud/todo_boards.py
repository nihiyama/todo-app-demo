from app.crud.base import CRUDBase
from app.models.todo_board import TodoBoard
from app.schemas.todo_board import TodoBoardCreate, TodoBoardUpdate


class CRUDUser(CRUDBase[TodoBoard, TodoBoardCreate, TodoBoardUpdate]):
    pass

todo_board = CRUDUser(TodoBoard)
