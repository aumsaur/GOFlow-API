from pydantic import BaseModel, EmailStr
from typing import Union, Dict, Any
from typing import Type
from datetime import datetime


class ItemBase(BaseModel):
    title: str


class ItemCreate(ItemBase):
    owner_id: str
    startupdata: Dict[str, Any] | None = None


class ItemUpdate(ItemBase):
    itemdata: Dict[str, Any] | None = None


class ItemInDBBase(ItemCreate, ItemUpdate):
    id: str
    created: datetime
    edited: datetime

    class Config:
        orm_mode = True
        exclude = ['startupdata']


class ItemGet(ItemInDBBase):
    pass


class ItemInDB(ItemInDBBase):
    pass
