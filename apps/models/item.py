# from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, JSON, String, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from apps.azure.base_model import Base
# from .user import User

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class Item(Base):
    id = Column(String(255), primary_key=True, index=True, unique=True)
    owner_id = Column(String(255), ForeignKey("user.id"), index=True)
    title = Column(String, index=False)
    created = Column(String, index=False)
    edited = Column(String, index=False)
    itemdata = Column(JSON, index=False)

    owner = relationship("User", back_populates="items")

    __table_args__ = (
        ForeignKeyConstraint(
            ['owner_id'],
            ['user.id'],
            name='item_owner_fk'
        ),
        UniqueConstraint('id', name='uq_item_id')
    )
