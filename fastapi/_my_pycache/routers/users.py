
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional
import sys
import os

# Add parent paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import MongoDB client
try:
    from db.client import users_collection
    MONGODB_AVAILABLE = True
except (ImportError, Exception) as e:
    print(f"Warning: MongoDB connection not available: {e}")
    users_collection = None
    MONGODB_AVAILABLE = False


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str


router = APIRouter()

# In-memory fallback database
in_memory_users = [
    {"_id": "1", "name": "Alejandro", "email": "alejandro@example.com"},
    {"_id": "2", "name": "Jorge", "email": "jorge@example.com"},
    {"_id": "3", "name": "Ana", "email": "ana@example.com"}
]


# Helper functions
def search_user_by_id(user_id: str):
    """Search user by ID"""
    if MONGODB_AVAILABLE:
        try:
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            return user
        except InvalidId:
            return None
    else:
        return next((u for u in in_memory_users if u["_id"] == user_id), None)


def search_user_by_name(name: str):
    """Search user by name"""
    if MONGODB_AVAILABLE:
        return users_collection.find_one({"name": name})
    else:
        return next((u for u in in_memory_users if u["name"] == name), None)


def get_all_users():
    """Get all users"""
    if MONGODB_AVAILABLE:
        users = []
        for user in users_collection.find():
            user["id"] = str(user["_id"])
            users.append(user)
        return users
    else:
        return in_memory_users


# Endpoints
@router.get("/users")
async def list_users():
    """Get all users"""
    return get_all_users()


@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user by ID"""
    user = search_user_by_id(user_id)
    if user:
        if MONGODB_AVAILABLE:
            user["id"] = str(user["_id"])
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.get("/usersquery/")
async def user_query(name: str):
    """Search user by name"""
    user = search_user_by_name(name)
    if user:
        if MONGODB_AVAILABLE:
            user["id"] = str(user["_id"])
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    """Create a new user"""
    if MONGODB_AVAILABLE:
        # Check if user with same email already exists
        existing_user = users_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create new user document
        user_dict = {"name": user.name, "email": user.email}
        result = users_collection.insert_one(user_dict)
        
        # Return created user with ID
        created_user = users_collection.find_one({"_id": result.inserted_id})
        created_user["id"] = str(created_user["_id"])
        return created_user
    else:
        # Fallback to in-memory storage
        existing_user = next((u for u in in_memory_users if u["email"] == user.email), None)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        new_user = {
            "_id": str(len(in_memory_users) + 1),
            "id": str(len(in_memory_users) + 1),
            "name": user.name,
            "email": user.email
        }
        in_memory_users.append(new_user)
        return new_user


@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    """Update user"""
    if MONGODB_AVAILABLE:
        try:
            object_id = ObjectId(user_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        result = users_collection.update_one(
            {"_id": object_id},
            {"$set": {"name": user.name, "email": user.email}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        updated_user = users_collection.find_one({"_id": object_id})
        updated_user["id"] = str(updated_user["_id"])
        return updated_user
    else:
        # Fallback to in-memory storage
        for saved_user in in_memory_users:
            if saved_user["_id"] == user_id:
                saved_user["name"] = user.name
                saved_user["email"] = user.email
                return saved_user
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Delete user"""
    if MONGODB_AVAILABLE:
        try:
            object_id = ObjectId(user_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        result = users_collection.delete_one({"_id": object_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "User deleted successfully"}
    else:
        # Fallback to in-memory storage
        for index, saved_user in enumerate(in_memory_users):
            if saved_user["_id"] == user_id:
                del in_memory_users[index]
                return {"message": "User deleted successfully"}
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) 