import bcrypt
from auth import create_access_token
from fastapi import FastAPI, Depends, HTTPException
from models.userModel import *
from sqlalchemy.orm import Session
from database import *


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/v0/user/register")  # create new user; POST
async def register_user(register: User, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.username == register.username) | (User.email == register.email)).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username or email already exists")
    hashed_password = bcrypt.hashpw(
        register.password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=register.username,
                    email=register.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"access_token": create_access_token(data={"sub": new_user.username}), "token_type": "bearer"}


@app.post("/api/v0/user/login")
async def login_user(login: User, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.username == login.username) | (User.email == login.email)).first()
    if db_user is None:
        raise HTTPException(
            status_code=400, detail="Incorrect username or email or password")
    if not bcrypt.checkpw(login.password.encode('utf-8'), db_user.password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or email or password")
    return {"access_token": create_access_token(data={"sub": db_user.username}), "token_type": "bearer"}


@app.get("/api/v0/{username}")  # get user info/profile; GET
async def fetch_user(token: str, db: Session = Depends(get_db)):
    # query the user's information from the database using the token
    result = db.execute("SELECT email, fName, age FROM users WHERE token = :token", {
                        "token": token}).fetchone()
    if result:
        return {"email": result[0], "name": result[1], "age": result[2]}
    else:
        raise HTTPException(status_code=401, detail="Invalid token.")


@app.put("/api/v0/user={user_id}")  # update/edit user info/profile; PUT
async def edit_user():
    # update/edit user to database at user

    return  # notice


@app.delete("/api/v0/user={user_id}")  # remove user account; DEL
async def delete_user(username: str):

    return  # notice
