from pydantic import BaseModel, EmailStr
from typing import Dict, Any
from enum import Enum
from datetime import datetime


# class Item(BaseModel):
#     itemdata: Dict
#     uuid: str
#     owner: EmailStr
#     member: EmailStr
#     created: datetime
#     edited: datetime


class Item(BaseModel):
    uid: str  # uid
    itemdata: Dict[str, Any]


class ItemCreate(Item):
    created: datetime
    edited: datetime


class ItemEdited(ItemCreate):
    pass
