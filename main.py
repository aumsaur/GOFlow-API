from typing import List

from fastapi import FastAPI

from models import User, Gender, Role

app = FastAPI()

db: List[User] = [
    User(
        username="username00",
        password="",
        first_name="Romtam",
        last_name="Tanpituckpong",
        gender=Gender.male,
        role=[Role.user, Role.admin])
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"username": user.username}
