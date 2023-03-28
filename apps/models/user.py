from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

# from pydantic import validator

from apps.azure.base_model import Base
# from schemas.user import UserType


class User(Base):
    id = Column(String, primary_key=True, index=False, nullable=False)
    email = Column(String, primary_key=True, index=True, nullable=False)
    type = Column(String, index=False)  # True for App
    displayname = Column(String, index=False)
    hashed_password = Column(String, nullable=True, index=False)

    items = relationship("Item", back_populates="owner")
