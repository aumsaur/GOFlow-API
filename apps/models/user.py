from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from apps.azure.base_model import Base


class User(Base):
    id = Column(String(255), primary_key=True, index=True)
    email = Column(String)
    user_type = Column(String, index=False)
    displayname = Column(String, index=False)
    hashed_password = Column(String, nullable=True, index=False)

    items = relationship("Item", back_populates="owner")
