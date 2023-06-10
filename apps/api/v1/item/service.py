import json
from typing import Any, List

from fastapi import APIRouter, HTTPException, Request, status, Depends, Body
from sqlalchemy.orm import Session


from apps import crud, models, schemas
from apps.api import deps


router = APIRouter()


@router.post("/create", response_model=schemas.ItemGet)
def create_item(request: Request, db: Session = Depends(deps.get_db), *, item: schemas.ItemCreate):
    return crud.item.create(db=db, obj_in=item, owner_id=request.state.token_sub.get('id'))


@router.get("/read/{item_id}", response_model=schemas.ItemGet)
def read_item(request: Request, db: Session = Depends(deps.get_db), *, item_id: str):
    db_item = crud.item.get(db=db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.owner_id != request.state.token_sub.get('id'):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db_item


@router.get("/fetch", response_model=List[schemas.ItemGet])
def fetch_item(request: Request, db: Session = Depends(deps.get_db)):

    owned_item = crud.item.get_by_owner(
        db=db, owner=request.state.token_sub.get('id'))
    if owned_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return owned_item


@router.put("/update", response_model=schemas.ItemGet)
def update_item(request: Request, db: Session = Depends(deps.get_db), *, item_id: str = Body(...), item: schemas.ItemUpdate):
    db_item = crud.item.get(db=db, id=item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return crud.item.update(db=db, db_obj=db_item, obj_in=item)


@router.delete("/delete")  # , response_model=schemas.ItemGet)
def delete_item(request: Request, db: Session = Depends(deps.get_db), *, item_id: str = Body(...)):
    db_item = crud.item.get(db=db, id=item_id)
    print('owner:', request.state.token_sub)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.owner_id != request.state.token_sub.get('id'):  # not owner
        print('not owner')
    #     raise HTTPException(
    #         status_code=403, detail="You do not have permission to delete this item")
    # return crud.item.delete(db=db, item_id=item_id)
    print(db_item.owner_id, request.state.token_sub.get('id'))
    return db_item


@router.get("/fetch/all", response_model=List[schemas.ItemGet], tags=["Debugs"])
def fetch_all_items(db: Session = Depends(deps.get_db), *, skip: int = 0, limit: int = 100):
    items = crud.item.get_multi(db, skip=skip, limit=limit)
    return items
