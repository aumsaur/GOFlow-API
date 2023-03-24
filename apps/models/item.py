from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, JSON, String
from sqlalchemy.orm import relationship

from azure.base_class import Base

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class Item(Base):
    uid = Column(String, primary_key=True, index=True, unique=True)
    owner = Column(String, index=True)
    title = Column(String)
    created = Column(String)
    edited = Column(String)
    metadata = Column(JSON)
