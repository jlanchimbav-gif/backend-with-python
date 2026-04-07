from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext

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
async def current_user(token: str = Depends(oauth2_scheme)):
    user = search_user_db(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})
    return user

# Endpoints
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_record = search_user_db(form_data.username)
    if not user_record:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password")
    
    if not crypt.verify(form_data.password, user_record.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password")
    
    return {
        "access_token": user_record.username,
        "token_type": "bearer"
    }

