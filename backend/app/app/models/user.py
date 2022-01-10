from typing import Counter
from sqlalchemy import (
    Column, Integer, String,
    DateTime, func
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from app.db.database import Base
from app.models.user_todo_card_map import user_todo_card_map_table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(32), unique=True, index=True, nullable=False)
    email_address = Column(String(256), unique=True, index=True, nullable=False)
    user_name = Column(String(256), index=True, nullable=False)
    hashed_password = Column(String, unique=True, nullable=False)
    is_superuser = Column(Boolean, default=False)

    todo_boards = relationship(
        "UserTodoBoardAssociation",
        back_populates="users"
    )

    todo_cards = relationship(
        "TodoCard",
        secondary=user_todo_card_map_table,
        primaryjoin=(user_todo_card_map_table.c.user_id == id),
        back_populates="assignees"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
