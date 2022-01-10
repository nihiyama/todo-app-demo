from sqlalchemy import (
    Column, ForeignKey, Integer, String, Text,
    Date, DateTime, func
)
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.user_todo_card_map import user_todo_card_map_table


class TodoCard(Base):
    __tablename__ = "todo_cards"

    id = Column(Integer, primary_key=True, index=True)
    todo_list_id = Column(Integer, ForeignKey("todo_lists.id"), index=True)
    title = Column(String(256))
    detail = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    assinees = relationship(
        "User",
        secondary=user_todo_card_map_table,
        primaryjoin=(user_todo_card_map_table.c.todo_card.id == id),
        back_populates="todo_cards"
    )

    todo_list = relationship(
        "TodoList",
        back_populates="todo_cards"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    