from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

engine = create_engine("sqlite:///mockup_azure_sql.db",
                       connect_args={"check_same_thread": False})

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
