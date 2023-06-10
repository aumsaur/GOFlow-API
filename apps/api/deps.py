from typing import Generator
from apps.azure.session import session


def get_db() -> Generator:
    try:
        db = session()
        yield db
    finally:
        db.close()
