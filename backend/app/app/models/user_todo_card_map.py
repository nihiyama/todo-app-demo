from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db.database import Base


user_todo_card_map_table = Table(
    "user_todo_card_map",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("card_id", Integer, ForeignKey("todo_card.id"))
)
