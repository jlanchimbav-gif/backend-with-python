from fastapi import FastAPI
from pydantic import BaseModel

app= FastAPI()

class User(BaseModel):
   username: str
   name= str
   surname=str
   email: str
   age: int
   disabled: bool

user_db={"JaguarEW": {
    "username": "JaguarEW",
    "name": "Alejandro",
    "surname": "Lanchimba",
    "email": "jlanchimbav@unemi.edu.ec",
    "age": 26,
    "disabled": False
}}