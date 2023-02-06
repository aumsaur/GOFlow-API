from fastapi import FastAPI
from typing import List

app = FastAPI()


@app.post("/api/v0/project={puid}")  # create project; POST
async def create_project(owner=str, puid=str):  # owner = user_id, puid= project uid
    # generate project
    # project uid
    # assign owner
    # assign init data
    return


@app.get("/api/v0/dashboard={username}")  # get project from user; GET
async def get_project(user_id=str):  # user_id = user_id
    # fetch project that associate with user
    return


@app.get("/api/v0/project={puid}/member")  # get project's associate user; GET
async def get_member(puid=str):  # puid = project uid
    # fetch user in certain project
    return


# add user to project; PUT
# invite link with constraint or else


@app.put("/api/v0/project={puid}/edit")  # update project; PUT
async def edit_project(puid=str):  # puid = project uid
    # update project
    return


@app.post("/api/v0/project={puid}/edit")  # remove project; DEL
async def remove_project(puid=str):  # puid = project uid
    return


@app.post("/api/v0/project={puid}/edit")  # create owner of project; POST
async def remove_project(puid=str):
    return
# add user to project with hierachy user; PUT
# remove user from project with hierachy user; DEL
# get project's user with hierachy user; GET
