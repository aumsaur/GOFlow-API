from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from apps.core.credentials import azure_setting

# engine = create_engine(azure_setting.CONNECT_STR)

engine = create_engine("sqlite:///mockup_azure_sql.db",
                       connect_args={"check_same_thread": False})

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
