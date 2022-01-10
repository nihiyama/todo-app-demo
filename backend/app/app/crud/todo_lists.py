from app.crud.base import CRUDBase
from app.models.todo_list import TodoList
from app.schemas.todo_list import TodoListCreate, TodoListUpdate


class CRUDUser(CRUDBase[TodoList, TodoListCreate, TodoListUpdate]):
    pass

todo_list = CRUDUser(TodoList)
