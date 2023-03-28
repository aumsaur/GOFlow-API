from typing import (
    Union,
    Optional,
    List,
    List,
    Dict,
    Any
)

from .crud_base import CRUDBase
from apps.models.item import Item
from apps.schemas.item import ItemCreate, ItemUpdate, ItemGet
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from datetime import datetime

import uuid


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create(self, db: Session, *, obj_in: ItemCreate) -> ItemGet:
        db_obj = Item(
            owner_id=obj_in.owner_id,
            title=obj_in.title,
            itemdata=obj_in.startupdata
        )
        db_obj.created = datetime.utcnow()
        db_obj.edited = datetime.utcnow()

        new_id = uuid.uuid4().hex

        while db.query(Item).filter(Item.id == new_id).first():
            new_id = uuid.uuid4().hex

        db_obj.id = new_id

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        item = ItemGet(
            id=db_obj.id,
            created=db_obj.created,
            edited=db_obj.edited,
            owner_id=db_obj.owner_id,
            title=db_obj.title,
            itemdata=db_obj.itemdata
        )

        return item

    def get_by_id(self, db: Session, id: str) -> ItemGet:
        db_obj = self.get(db, id)
        return ItemGet.from_orm(db_obj) if db_obj else None

    # def get_by_owner(self, db: Session, owner: str, skip: int = 0, limit: int = 100) -> Optional[List[ItemGet]]:
    #     return db.query(Item).filter(Item.owner_id == owner).offset(skip).limit(limit).all()

    def get_by_owner(self, db: Session, owner: str) -> Optional[List[ItemGet]]:
        db_items = db.query(Item).filter(Item.owner_id == owner).all()
        items = [ItemGet.from_orm(item) for item in db_items]
        return items or None

    def update(self, db: Session, *, db_obj: Item, obj_in: Union[ItemUpdate, Dict[str, Any]]) -> ItemGet:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data["updated"] = datetime.utcnow()
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete(self, db: Session, *, item_id: str) -> ItemGet:
        db_obj = self.get(db, item_id)
        if not db_obj:
            raise ValueError(f"Item with id '{item_id}' not found")
        item = ItemGet.from_orm(db_obj)
        db.delete(db_obj)
        db.commit()
        return item


item = CRUDItem(Item)
