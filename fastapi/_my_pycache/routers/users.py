
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str


router = APIRouter()

# In-memory database
user_list = [
    User(id=1, name="Alejandro", email="alejandro@example.com"),
    User(id=2, name="Jorge", email="jorge@example.com"),
    User(id=3, name="Ana", email="ana@example.com")
]


# Helper function
def search_user(user_id: int):
    user = filter(lambda u: u.id == user_id, user_list)
    try:
        return list(user)[0]
    except IndexError:
        return None


# Endpoints
@router.get("/")
async def list_users():
    return user_list


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = search_user(user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.get("/usersquery/")
async def user_query(name: str):
    user = next((u for u in user_list if u.name == name), None)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if search_user(user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    user_list.append(user)
    return user


@router.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user_id:
            user_list[index] = user
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for index, saved in enumerate(user_list):
        if saved.id == user_id:
            del user_list[index]
            return {"message": "User deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    ) 