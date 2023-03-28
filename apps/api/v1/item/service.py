from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session


from apps import crud, models, schemas
from apps.api import deps


router = APIRouter()


@router.post("/create/", response_model=schemas.ItemGet)
def create_item(db: Session = Depends(deps.get_db), *, item: schemas.ItemCreate):
    return crud.item.create(db=db, obj_in=item)


@router.get("/fetch/all", response_model=List[schemas.ItemGet])
def fetch_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    items = crud.item.get_multi(db, skip=skip, limit=limit)
    return items


@router.get("/read/{item_id}", response_model=schemas.ItemGet)
def read_item(item_id: str, db: Session = Depends(deps.get_db)):
    db_item = crud.item.get(db=db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/fetch/{owner_id}", response_model=schemas.ItemGet)
def fetch_item(owner_id: str, db: Session = Depends(deps.get_db)):
    owned_item = crud.item.get_by_owner(db=db, owner=owner_id)
    if owned_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return owned_item


@router.put("/update/{item_id}", response_model=schemas.ItemGet)
def update_item(item_id: str, item: schemas.ItemUpdate, db: Session = Depends(deps.get_db)):
    db_item = crud.item.get(db=db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.item.update(db=db, db_obj=db_item, obj_in=item)


@router.delete("/delete/{item_id}", response_model=schemas.ItemGet)
def delete_item(item_id: str, db: Session = Depends(deps.get_db)):
    db_item = crud.item.get(db=db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.item.delete(db=db, item_id=item_id)
