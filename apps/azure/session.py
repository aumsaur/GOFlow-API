from typing import Any

from sqlalchemy.ext.declarative import (
    as_declarative,
    declared_attr
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from apps.schemas.user import UserDB

engine = create_engine("sqlite:///:memory:", echo=True)


# @as_declarative()
# class Base:
#     id: Any
#     __name__: str
#     # Generate __tablename__ automatically

#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()


# Base.metadata.create_all(bind=engine)

_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = _Session()
