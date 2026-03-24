from http.client import HTTPException

from fastapi import FastAPI
from fastapi._my_pycache.routers.users import search_user
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import FastAPI
from tkinter.tix import Form


app= FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
   username: str
   name= str
   surname=str
   email: str
   age: int
   disabled: bool

class UserDB(User):
    password: str

user_db = {
    "JaguarEW": {
        "username": "JaguarEW",
        "name": "Alejandro",
        "surname": "Lanchimba",
        "email": "jlanchimbav@unemi.edu.ec",
        "age": 26,
        "disabled": False
    },
    "Jaguarking": {
        "username": "Jaguarking",
        "name": "Jorge",
        "surname": "vivas",
        "email": "jvivas@unemi.edu.ec",
        "age": 30,
        "disabled": True
    }
}

def search_user_db(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    return None

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
     user_db = search_user_db(form_data.username)
     if not user_db:
         raise HTTPException(
            status_code=400, detail="Incorrect username or password")

user= search_user(Form.username)
if Form.password != user.password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
        
return({"access_token": user.username, "token_type": "bearer"})