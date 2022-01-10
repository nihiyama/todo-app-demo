from sqlalchemy import (
    Column, Integer, String, Text,
    DateTime, func
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class TodoBoard(Base):
    __tablename__ = "todo_boards"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(32), unique=True, index=True, nullable=False)
    title = Column(String(256))
    detail = Column(Text, nullable=True)
    list_order = Column(String)

    users = relationship(
        "UserTodoBoardAssociation",
        back_populates="todo_boards"
    )

    todo_lists = relationship(
        "TodoList",
        back_populates="todo_board"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
