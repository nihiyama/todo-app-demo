from app.crud.base import CRUDBase
from app.models.todo_card import TodoCard
from app.schemas.todo_card import TodoCardCreate, TodoCardUpdate


class CRUDUser(CRUDBase[TodoCard, TodoCardCreate, TodoCardUpdate]):
    pass

todo_card = CRUDUser(TodoCard)
