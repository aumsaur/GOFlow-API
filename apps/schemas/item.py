from pydantic import BaseModel, EmailStr
from typing import Union, Dict, Any
# from enum import Enum
from datetime import datetime


class ItemBase(BaseModel):
    title: str


class ItemCreate(ItemBase):
    owner: EmailStr
    created: datetime


class ItemUpdate(ItemBase):
    updated: datetime
    metadata: Dict[str, Any]


class ItemInDBBase(Union[ItemCreate, ItemUpdate]):
    item_uid: str  # uid

    class Config:
        orm_mode = True


class ItemGet(ItemInDBBase):
    pass


class ItemInDB(ItemInDBBase):
    pass
