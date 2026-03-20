
from http.client import HTTPException

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str


router = APIRouter()
app = FastAPI()

@router.get("/")
async def users():
    return [User(id=1, name="Alejandro", email="alejandro@example.com"),
            User(id=2, name="jorge", email="jorge@example.com"),
            User(id=3, name="Ana", email="ana@example.com")]

@router.get("/users/{user_id}")
async def userclass(user_id: int):
    return User(id=user_id, name="User " + str(user_id), email=f"user{user_id}@example.com")
  
user_list = [User(id=1, name="Alejandro", email="alejandro@example.com"),
             User(id=2, name="jorge", email="jorge@example.com"),
             User(id=3, name="Ana", email="ana@example.com")]

@router.get("/users/{user_id}/")
async def get_user(user_id: int):
    user = filter(lambda u: u.id == user_id, user_list)
    try:
        return list(user)[0]
    except IndexError:
        return {"error": "User not found"}

@router.get("/usersquery/")
async def user_query(name: str):
    user = filter(lambda user: user.name == name, user_list)
    try:
        return list(user)[0]
    except IndexError:
        return {"error": "User not found"}

@router.post("/users/", status_code=201)
async def user(user: User):
    if type (search_user(user.id)) == User:
        return {"error": "User already exists"}
    else :
        user_list.append(user)
        return user


def search_user(user_id: int):
    user = filter(lambda user: user.id == user_id, user_list)
    try:
        return list(user)[0]
    except IndexError:
        return None

@app.put("/users/")
async def update_user(user: User):
    found = False
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            found = True
            break
    if not found:
        return {"error": "User not found"}
    return user
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for index , saved in enumerate(user_list):
        if saved.id == user_id:
            del user_list[index]
            return {"message": "User deleted"}
    return {"error": "User not found"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    found=False
    for index, saved in enumerate(user_list):
        if saved.id == user_id:
            del user_list[index]
            found = True
            break
    if not found:
        return {"error": "User not found"}
    return {"message": "User deleted"}

## http status code ##

user_list = []
@app.post("/users/", status_code=201)
async def user(user: User):
    if type (search_user(user.id)) == User:
     raise HTTPException(status_code=400, detail="User already exists")

user_list.append(user)
return user