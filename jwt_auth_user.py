from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional

# Configuration
ALGORITHMS = ["HS256"]
SECRET_KEY = "your-secret-key-change-in-production"
ACCESS_TOKEN_DURATION = 30  # minutes

# Security - Password hashing
crypt = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt-auth/token")

# Create router for JWT authentication
router = APIRouter(prefix="/jwt-auth", tags=["jwt-authentication"])

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

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None

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
    """Search user in database with password"""
    if username in user_db:
        return UserDB(**user_db[username])
    return None

def search_user(username: str):
    """Search user without exposing password"""
    if username in user_db:
        return User(**{k: v for k, v in user_db[username].items() if k != 'password'})
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHMS[0])
    return encoded_jwt

# Authentication dependencies
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate JWT token and return current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHMS)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = search_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    """Check if current user is active"""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user")
    return current_user

# Endpoints
@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint - returns JWT token"""
    user_db_record = search_user_db(form_data.username)
    if not user_db_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})
    
    if not crypt.verify(form_data.password, user_db_record.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})
    
    if user_db_record.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = create_access_token(
        data={"sub": user_db_record.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_DURATION * 60
    }

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user information"""
    return current_user

@router.get("/users/{username}", response_model=User)
async def get_user_info(
    username: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get user information (requires authentication)"""
    user = search_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")
    return user

@router.post("/token/validate")
async def validate_token(current_user: User = Depends(get_current_active_user)):
    """Validate if token is still valid"""
    return {
        "valid": True,
        "username": current_user.username,
        "message": "Token is valid"
    }



