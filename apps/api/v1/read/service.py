from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from apps.schemas.item import ItemCreate
from datetime import datetime

from typing import Dict


fake_item_db = {}


router = APIRouter()


@router.post("/api/v1/items/")
async def create_item():

    # fake_item_db[uuid.uuid4().hex] = jsonable_encoder(item) add item with crud

    return


@router.post("/api/v1/items/{item_id}")
async def update_item(item_id: str, itemdata_edited: Dict):
    # if item_id in fake_item_db: update with crud
    #     fake_item_db[item_id]["itemdata"] = itemdata_edited
    #     fake_item_db[item_id]["created"] = datetime.utcnow()
    return itemdata_edited


@router.get("/api/v1/items/{item_id}")
async def read_item(item_id: str):
    if item_id in fake_item_db:
        return fake_item_db[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/api/v1/items/all/")
async def read_all_item():
    return fake_item_db
