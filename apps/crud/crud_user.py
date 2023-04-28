import uuid

from typing import (
    Union,
    Optional,
    Dict,
    Any
)

from .crud_base import CRUDBase
from sqlalchemy.orm import Session

from apps.core.security import get_hashed_password, verify_password
from apps.models.user import User
from apps.schemas.user import UserCreate, UserUpdate, UserGet, UserType


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> UserGet:
        db_obj = User(
            id=uuid.uuid4().hex,
            email=obj_in.email,
            user_type=obj_in.user_type,
            displayname=obj_in.displayname,
            hashed_password=get_hashed_password(
                obj_in.password) if obj_in.user_type == UserType.app else None
        )
        print(db_obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return UserGet(id=db_obj.id, displayname=db_obj.displayname, email=db_obj.email, user_type=db_obj.user_type)

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserGet]:
        # return db.query(User).filter(User.email == email).first()
        db_obj = db.query(User).filter(User.email == email).first()
        return UserGet.from_orm(db_obj) if db_obj else None

    def get_by_id(self, db: Session, *, id: str) -> Optional[UserGet]:
        # return db.query(User).filter(User.email == email).first()
        db_obj = db.query(User).filter(User.email == id).first()
        return UserGet.from_orm(db_obj) if db_obj else None

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> UserGet:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_hashed_password(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        # return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str = None, type: UserType = UserType.app) -> Optional[UserGet]:
        # user = self.get_by_email(db, email=email)
        user = db.query(User).filter(User.email == email).first()
        print(user.user_type + ': ' + UserType.app)
        if not user:
            return None
        if not verify_password(password, user.hashed_password) and user.user_type is UserType.app:
            return None
        return UserGet(displayname=user.displayname, email=user.email, user_type=user.user_type, id=user.id)

    def remove(self, db: Session, *, id: str) -> UserGet:
        return super().remove(db, id=id)


user = CRUDUser(User)
