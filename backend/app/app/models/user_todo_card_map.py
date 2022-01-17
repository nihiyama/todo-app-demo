from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db.database import Base


user_todo_card_map_table = Table(
    "user_todo_card_map",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("todo_card_id", Integer, ForeignKey("todo_cards.id"))
)
