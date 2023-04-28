from typing import List

from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session


from apps import crud, models, schemas
from apps.core.security import verify_access_token
from apps.api import deps


router = APIRouter()


@router.post("/create", response_model=schemas.ItemGet)
def create_item(db: Session = Depends(deps.get_db), *, item: schemas.ItemCreate):
    return crud.item.create(db=db, obj_in=item)


@router.get("/read/{item_id}", response_model=schemas.ItemGet)
def read_item(db: Session = Depends(deps.get_db), *, item_id: str):
    # TODO: authenticate user
    db_item = crud.item.get(db=db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/fetch/{owner_id}", response_model=schemas.ItemGet)
def fetch_item(db: Session = Depends(deps.get_db), *, owner_id: str):
    # def fetch_item(db: Session = Depends(deps.get_db), *, owner_id: str, access_token: dict):
    # TODO: authenticate user
    # checking if token expire
    # if (verify_access_token(access_token)):
    # return  # unauthentucated TODO: re-authenticated
    # get owner id from token

    #
    owned_item = crud.item.get_by_owner(db=db, owner=owner_id)
    if owned_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return owned_item


@router.put("/update/{item_id}", response_model=schemas.ItemGet)
def update_item(db: Session = Depends(deps.get_db), *, item_id: str, item: schemas.ItemUpdate):
    # TODO: authenticate
    db_item = crud.item.get(db=db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.item.update(db=db, db_obj=db_item, obj_in=item)


@router.delete("/delete/{item_id}", response_model=schemas.ItemGet)
def delete_item(item_id: str, db: Session = Depends(deps.get_db)):
    # TODO: authenticate
    db_item = crud.item.get(db=db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.item.delete(db=db, item_id=item_id)


@router.get("/fetch/all", response_model=List[schemas.ItemGet])
def fetch_all_items(db: Session = Depends(deps.get_db), *, skip: int = 0, limit: int = 100):
    items = crud.item.get_multi(db, skip=skip, limit=limit)
    return items
# {
# "access_token": create_access_token(
#     {"sub": user.json()}, expires_delta = access_token_expires),
# "token_type": "bearer", "status": status.HTTP_200_OK
# }
#
# TODO: authenticate by
# pass access token to parameter then decode in backend
# or remember session in backend then use the session to authenticate
