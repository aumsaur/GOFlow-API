from pydantic import BaseModel, EmailStr
from typing import Union, Dict, Any
from typing import Type
from datetime import datetime


class ItemBase(BaseModel):
    title: str
    itemdata: Dict[str, Any] | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemInDBBase(ItemCreate, ItemUpdate):
    id: str
    owner_id: str
    created: datetime
    edited: datetime

    class Config:
        orm_mode = True


class ItemGet(ItemInDBBase):
    pass
    # class Config:
    # exclude = {'init_data'}
    # exclude = ['init_data']
    # fields = {'init_data': {'exclude': True}}


class ItemInDB(ItemInDBBase):
    pass
