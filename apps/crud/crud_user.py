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
            type=obj_in.user_type,
            displayname=obj_in.displayname,
            hashed_password=get_hashed_password(
                obj_in.password) if obj_in.user_type == UserType.app else None
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return UserGet(id=db_obj.id, displayname=db_obj.displayname, email=db_obj.email, user_type=db_obj.type)

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> UserGet:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_hashed_password(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str = None) -> Optional[UserGet]:
        user = self.get_by_email(db, email=email)
        print(user.type + ': ' + UserType.app)
        if not user:
            return None
        if not verify_password(password, user.hashed_password) and user.type is UserType.app:
            return None
        return UserGet(displayname=user.displayname, email=user.email, user_type=user.type, id=user.id)


user = CRUDUser(User)
