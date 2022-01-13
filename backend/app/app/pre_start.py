import logging

from sqlalchemy.orm.session import Session
from tenacity import (
    after_log, before_log, retry,
    stop_after_attempt, wait_fixed
)

from app.db.database import SessionLocal


logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN)
)
def init() -> None:
    try:
        db: Session = SessionLocal()
        db.execute("SELECT 1")
    finally:
        db.close()


def main() -> None:
    init()


if __name__ == "__main__":
    main()
