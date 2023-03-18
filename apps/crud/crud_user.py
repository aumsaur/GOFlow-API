from typing import (
    Union,
    Optional,
    Dict,
    Any
)

from crud_base import CRUDBase
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserType
from sqlalchemy.orm import Session
from core.secure import get_hashed_password, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        if (obj_in.user_type == UserType.app):
            db_obj = User(
                email=obj_in.email,
                hashed_password=get_hashed_password(obj_in.password)
            )
        elif (obj_in.user_type == UserType.google):
            obj_in = User(
                email=obj_in.email,

            )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_hashed_password(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str = None) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

#     def is_superuser(self, user: User) -> bool:
#         return user.is_superuser


user = CRUDUser(User)
