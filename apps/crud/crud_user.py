from typing import Union, Optional
from sqlalchemy.orm import Session

from .crud_base import CRUDBase

from apps.core.security import get_hashed_password, verify_password
from apps.models.user import User
from apps.schemas.user import (
    UserCreate,
    UserUpdateProfile,
    UserUpdatePassword,
    UserGet,
    UserType
)

import uuid


class CRUDUser(CRUDBase[User, UserCreate, UserUpdateProfile]):
    def create(self, db: Session, *, obj_in: UserCreate) -> UserGet:
        """
        Create a new user.

        Parameters:
        - db (Session): The database session.
        - obj_in (UserCreate): The user creation details.

        Returns:
        - UserGet: The created user.
        """
        while True:
            new_id = uuid.uuid4().hex
            if not db.query(User).filter(User.id == new_id).first():
                break

        db_obj = User(
            id=new_id,
            email=obj_in.email,
            user_type=obj_in.user_type,
            displayname=obj_in.display_name,
            hashed_password=get_hashed_password(
                obj_in.password) if obj_in.user_type == UserType.app else None
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return UserGet(id=db_obj.id, display_name=db_obj.displayname, email=db_obj.email, user_type=db_obj.user_type)

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserGet]:
        """
        Get a user by email.

        Parameters:
        - db (Session): The database session.
        - email (str): The email of the user.

        Returns:
        - Optional[UserGet]: The user if found, None otherwise.
        """
        db_obj = db.query(User).filter(User.email == email).first()
        return UserGet.from_orm(db_obj) if db_obj else None

    def get_by_id(self, db: Session, *, id: str) -> Optional[UserGet]:
        db_obj = db.query(User).filter(User.id == id).first()
        return UserGet.from_orm(db_obj) if db_obj else None

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdateProfile, UserUpdatePassword]) -> UserGet:
        """
        Get a user by ID.

        Parameters:
        - db (Session): The database session.
        - id (str): The ID of the user.

        Returns:
        - Optional[UserGet]: The user if found, None otherwise.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "new_password" in update_data:
            hashed_password = get_hashed_password(update_data["new_password"])
            del update_data["new_password"]
            update_data["hashed_password"] = hashed_password
            db_obj = super().update(db, db_obj=db_obj, obj_in=update_data)
        return UserGet.from_orm(db_obj)

    def authenticate(self, db: Session, *, email: str, password: str = None, type: UserType = UserType.app) -> Optional[UserGet]:
        """
        Authenticate a user.

        Parameters:
        - db (Session): The database session.
        - email (str): The email of the user.
        - password (str): The password of the user (optional).
        - type (UserType): The type of the user (default: UserType.app).

        Returns:
        - Optional[UserGet]: The authenticated user if successful, None otherwise.
        """
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password) and user.user_type == UserType.app:
            return None
        return UserGet(display_name=user.displayname, email=user.email, user_type=user.user_type, id=user.id)

    def remove(self, db: Session, *, id: str) -> UserGet:
        """
        Remove a user.

        Parameters:
        - db (Session): The database session.
        - id (str): The ID of the user.

        Returns:
        - UserGet: The removed user.
        """
        return super().remove(db, id=id)


user = CRUDUser(User)
