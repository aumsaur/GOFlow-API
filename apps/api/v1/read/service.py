from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from apps.schemas.item import ItemCreate, ItemEdited
from datetime import datetime, timedelta

from typing import Dict, Any

import uuid
import json

fake_item_db = {}


router = APIRouter()


@router.post("/api/v1/items/")
async def create_item():
    uid = uuid.uuid4().hex
    item = ItemCreate(uid=uid, itemdata={}, created=datetime.utcnow(),
                      edited=datetime.utcnow())
    fake_item_db[uid] = jsonable_encoder(item)
    return item


@router.post("/api/v1/items/{item_id}")
async def update_item(item_id: str, itemdata_edited: Dict):
    if item_id in fake_item_db:
        fake_item_db[item_id]["itemdata"] = itemdata_edited
        fake_item_db[item_id]["created"] = datetime.utcnow()
    return itemdata_edited
    # print(itemdata_edited)
    # fake_item_db[item_id].itemdata = itemdata
    # return fake_item_db[item_id]
    # else:
    #     raise HTTPException(status_code=404, detail="Item not found")
    # if item_id in fake_item_db:
    #     edited_item = fake_item_db[item_id]
    #     edited_item['item_data'] = item_data_edited
    #     edited_item['edited'] = datetime.utcnow()
    #     # edited_item.itemdata = item_data_edited
    #     # edited_item.edited = datetime.utcnow()
    #     fake_item_db[item_id] = jsonable_encoder(edited_item)
    #     return fake_item_db[item_id]
    # else:
    #     raise HTTPException(status_code=404, detail="Item not found")

# @router.post("/api/v1/items/{item_id}")
# async def update_item(item_id: str):
#     if item_id in fake_item_db:
#         edited_item = fake_item_db[item_id]
#         edited_item['item_data'] = newjson
#         edited_item['edited'] = datetime.utcnow()
#         # edited_item.itemdata = item_data_edited
#         # edited_item.edited = datetime.utcnow()
#         fake_item_db[item_id] = jsonable_encoder(edited_item)
#         return fake_item_db[item_id]
#     else:
#         raise HTTPException(status_code=404, detail="Item not found")


# @router.post("/api/v1/items/dev")
# async def dev_item():
#     # if item_id in fake_item_db:
#     # itemdata = ItemEdited.parse_raw_as(dict, itemdata_edited)
#     return newjsondev


@router.get("/api/v1/items/{item_id}")
async def read_item(item_id: str):
    if item_id in fake_item_db:
        return fake_item_db[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/api/v1/items/all/")
async def read_all_item():
    return fake_item_db
