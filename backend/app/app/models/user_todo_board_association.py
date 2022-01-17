from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class UserTodoBoardAssociation(Base):
    __tablename__ = "user_todo_board_association"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    todo_board_id = Column(Integer, ForeignKey("todo_boards.id", ondelete="CASCADE"), primary_key=True)
    is_owner = Column(Boolean, default=False)

    user = relationship(
        "User",
        back_populates="todo_boards"
    )

    todo_board = relationship(
        "TodoBoard",
        back_populates="users"
    )

    