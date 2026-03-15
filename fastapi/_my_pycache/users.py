
from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str


app= FastAPI()

app.get("/")
async def users():
    return [User(id=1, name="Alejandro", email="alejandro@example.com"),
            User(id=2, name="jorge", email="jorge@example.com"),
            User(id=3, name="Ana", email="ana@example.com")]

@app.get("/users/{user_id}")
async def userclass(user_id: int):
    return User(id=user_id, name="User " + str(user_id), email=f"user{user_id}@example.com")
    