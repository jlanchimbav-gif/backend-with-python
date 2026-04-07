from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

# Configuration
ALGORITHMS = ["HS256"]
SECRET_KEY = "your-secret-key"
ACCESS_TOKEN_DURATION = 1

# Security
crypt = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Models
class User(BaseModel):
    username: str
    name: str
    surname: str
    email: str
    age: int
    disabled: bool

class UserDB(User):
    password: str

# Database
user_db = {
    "JaguarEW": {
        "username": "JaguarEW",
        "name": "Alejandro",
        "surname": "Lanchimba",
        "email": "jlanchimbav@unemi.edu.ec",
        "age": 26,
        "password": crypt.hash("password123"),
        "disabled": False
    },
    "Jaguarking": {
        "username": "Jaguarking",
        "name": "Jorge",
        "surname": "vivas",
        "email": "jvivas@unemi.edu.ec",
        "age": 30,
        "password": crypt.hash("password456"),
        "disabled": False
    }
}

# Helper functions
def search_user_db(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    return None

def search_user(username: str):
    if username in user_db:
        return User(**{k: v for k, v in user_db[username].items() if k != 'password'})
    return None

# Authentication
async def auth_user(token: str = Depends(oauth2_scheme)):
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHMS).get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})
    return username

async def current_user(token_user: str = Depends(auth_user)):
    user = search_user(token_user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found")
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user")
    return user

# Endpoints
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db_record = search_user_db(form_data.username)
    if not user_db_record:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password")
    
    if not crypt.verify(form_data.password, user_db_record.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password")
    
    access_token = {
        "sub": user_db_record.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    
    return {
        "access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHMS[0]),
        "token_type": "bearer"
    }



