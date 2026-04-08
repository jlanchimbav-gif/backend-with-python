from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
        "password": "password123",
        "disabled": False
    },
    "Jaguarking": {
        "username": "Jaguarking",
        "name": "Jorge",
        "surname": "vivas",
        "email": "jvivas@unemi.edu.ec",
        "age": 30,
        "password": "password456",
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
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = search_user_db(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return user

# Endpoints
@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint - returns token"""
    user_record = search_user_db(form_data.username)
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if form_data.password != user_record.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    return {
        "access_token": user_record.username,
        "token_type": "bearer"
    }

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return current_user

@router.get("/users/{username}", response_model=User)
async def get_user_info(username: str, current_user: User = Depends(get_current_user)):
    """Get user information (requires authentication)"""
    user = search_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


