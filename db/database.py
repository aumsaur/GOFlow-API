from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import json


Base = declarative_base()


class UserData(Base):
    __tablename__ = 'UserData'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    data = Column(String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.data = json.dumps({
            'username': username,
            'email': email,
            'password': password
        })


engine = create_engine('sqlite:///mockup_azure_sql.db')
# Base.metadata.create_all(engine)

# create a session local factory to manage database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def store_user_data(user_data: str):
    db = SessionLocal()
    user = UserData(data=user_data)
    db.add(user)
    db.commit()


def get_user_data(user_id: int):
    db = SessionLocal()
    user = db.query(UserData).get(user_id)
    return user.data
