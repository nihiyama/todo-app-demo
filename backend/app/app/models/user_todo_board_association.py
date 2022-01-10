from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class UserTodoBoardAssociation(Base):
    __tablename__ = "user_todo_board_association"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    todo_board_id = Column(Integer, ForeignKey("todo_boards.id"), primary_key=True)
    is_owner = Column(Boolean, default=False)

    users = relationship(
        "User",
        back_populates="todo_boards"
    )

    todo_boards = relationship(
        "TodoBoard",
        back_populates="users"
    )

    