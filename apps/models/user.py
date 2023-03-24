from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String, event
# from sqlalchemy.event import listen
from pydantic import validator

from apps.azure.base_class import Base

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class User(Base):
    email = Column(String, primary_key=True, unique=True,
                   index=True, nullable=False)
    type = Column(Boolean, index=True)  # True for App
    displayname = Column(String, index=True)
    hashed_password = Column(String, nullable=True)

    def __init__(self, email, type, displayname, hashed_password=None):
        self.email = email
        self.type = type
        self.displayname = displayname
        self.hashed_password = hashed_password

    @staticmethod
    def hashed_password_nullable(context):
        if not context['type']:
            return None
        else:
            return context.current_parameters['hashed_password']

    @validator('hashed_password')
    def validate_hashed_password(self, key, value):
        if not self.type:
            return None
        else:
            return value

    # Define the before_insert event
    @event.listens_for(Base, 'before_insert')
    def before_insert_listener(mapper, connection, target):
        # Validate the hashed_password before insert
        target.hashed_password = target.validate_hashed_password(
            'hashed_password', target.hashed_password)
