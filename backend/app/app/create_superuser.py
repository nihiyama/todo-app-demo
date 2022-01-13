from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.db.database import SessionLocal


def init() -> None:
    try:
        db: Session = SessionLocal()
        init_db(db)
    finally:
        db.close()


def main() -> None:
    init()


if __name__ == "__main__":
    main()