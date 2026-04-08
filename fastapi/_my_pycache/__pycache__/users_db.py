
from fastapi import APIRouter, HTTPException, status 
from db.models.users import User
from db.client import db_client
from fastapi._my_pycache.__pycache__.schemas.user import user_schema




router = APIRouter()

router=APIRouter(prefix="/userdb",
                    tags=["users-db"],
                    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

# In-memory database
user_list = []

@router.get("/",response_model=list[User])
async def users():
    return user_schema(db_client.local.users.find())





# Helper function
def search_user(user_id: int):
    user = filter(lambda u: u.id == user_id, user_list)
    try:
        return list(user)[0]
    except IndexError:
        return None


# Endpoints
@router.get("/usersdb")
async def list_users():
    return user_list


@router.get("/usersdb/{user_id}")
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


@router.post("/usersdb/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
   # if search_user(user.id):
      #   raise HTTPException(
    #        status_code=status.HTTP_400_BAD_REQUEST,
    #        detail="User already exists"
    #    )
    
    user_dict= user.dict()
    del user_dict["id"]
    
    id= db_client.users.insert_one(user_dict)
    new_user= db_client.local.users.find_one({"id": id})
    
    return user


@router.put("/usersdb/{user_id}")
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