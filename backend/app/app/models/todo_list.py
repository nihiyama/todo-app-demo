from sqlalchemy import (
    Column, ForeignKey, Integer, String, Text,
    DateTime, func
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class TodoList(Base):
    __tablename__ = "todo_lists"

    id = Column(Integer, primary_key=True, index=True)
    todo_board_id = Column(Integer, ForeignKey("todo_boards.id"), index=True)
    title = Column(String(256))
    detail = Column(Text, nullable=True)
    card_order = Column(String)

    todo_board = relationship(
        "TodoBoard",
        back_populates="todo_lists"
    )

    todo_cards = relationship(
        "TodoCard",
        back_populates="todo_list"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
