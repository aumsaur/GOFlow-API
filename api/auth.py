import json
import db.database as db
from fastapi import FastAPI, HTTPException
from models.userModel import User

app = FastAPI()


@app.post("/register")
def register_user(user: User):
    user_data = json.dumps(
        {"email": user.email, "username": user.username, "password": user.password})
    db.store_user_data(user_data)
    return {"message": "User registered successfully."}


@app.post("/login")
def login_user(user: User):
    user_data = db.get_user_data(user.username)
    if user_data is None:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password.")

    user_data = json.loads(user_data)
    if user_data["password"] != user.password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password.")

    return {"message": "Login successful."}
