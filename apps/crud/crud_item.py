from typing import Union, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from .crud_base import CRUDBase
from apps.models.item import Item
from apps.schemas.item import ItemCreate, ItemUpdate, ItemGet

import uuid


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create(self, db: Session, *, obj_in: ItemCreate, owner_id: str) -> ItemGet:
        """
        Create a new item.

        Parameters:
        - db (Session): The database session.
        - obj_in (ItemCreate): The item data for creation.
        - owner_id (str): The ID of the owner.

        Returns:
        - ItemGet: The created item.
        """
        while True:  # guarantee unduplicate uid
            new_id = uuid.uuid4().hex
            if not db.query(Item).filter(Item.id == new_id).first():
                break

        db_obj = Item(
            id=new_id,
            owner_id=owner_id,
            title=obj_in.title,
            item_data=obj_in.item_data,
            created=datetime.utcnow(),
            edited=datetime.utcnow(),
        )  # construct item to store in db

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return ItemGet(
            id=db_obj.id,
            created=db_obj.created,
            edited=db_obj.edited,
            owner_id=db_obj.owner_id,
            title=db_obj.title,
            item_data=db_obj.item_data
        )

    def get_by_id(self, db: Session, id: str) -> ItemGet:
        """
        Get an item by ID.

        Parameters:
        - db (Session): The database session.
        - id (str): The ID of the item.

        Returns:
        - Optional[ItemGet]: The retrieved item or None if not found.
        """
        db_obj = self.get(db, id)
        return ItemGet.from_orm(db_obj) if db_obj else None

    def get_by_owner(self, db: Session, owner: str) -> Optional[List[ItemGet]]:
        """
        Get items by owner.

        Parameters:
        - db (Session): The database session.
        - owner (str): The ID of the owner.

        Returns:
        - Optional[List[ItemGet]]: The retrieved items or None if not found.
        """
        db_items = db.query(Item).filter(Item.owner_id == owner).all()
        items = [ItemGet.from_orm(item) for item in db_items]
        return items or None

    def update(self, db: Session, *, db_obj: Item, obj_in: Union[ItemUpdate, Dict[str, Any]]) -> ItemGet:
        """
        Update an item.

        Parameters:
        - db (Session): The database session.
        - db_obj (Item): The item object from the database.
        - obj_in (Union[ItemUpdate, Dict[str, Any]]): The updated item data.

        Returns:
        - ItemGet: The updated item.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data["edited"] = datetime.utcnow()
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete(self, db: Session, *, item_id: str) -> ItemGet:
        """
        Delete an item.

        Parameters:
        - db (Session): The database session.
        - item_id (str): The ID of the item to delete.

        Returns:
        - ItemGet: The deleted item.

        Raises:
        - ValueError: If the item with the specified ID is not found.
        """
        db_obj = self.get(db, item_id)
        if not db_obj:
            raise ValueError(f"Item with id '{item_id}' not found")
        item = ItemGet.from_orm(db_obj)
        db.delete(db_obj)
        db.commit()
        return item


item = CRUDItem(Item)
