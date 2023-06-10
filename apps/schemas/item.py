from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class ItemBase(BaseModel):
    title: str
    item_data: Dict[str, Any] | None = {}


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


class ItemInDB(ItemInDBBase):
    pass
