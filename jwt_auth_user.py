from http.client import HTTPException
import token

from fastapi._my_pycache.routers.users import search_user, users
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHMS=["HS256"]
SECRET_KEY = "your-secret-key"
Access_TOKEN_DURATION=1

app= FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
crypt = CryptContext(schemes=["bcrypt"])


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
        "password": crypt.hash("$2a$12$86WweYoELk9OFriuztkjE.Zp4I5aoWMJVCmnV2A2e1ty1O0rcHGVa"),
        "disabled": False
    },
    "Jaguarking": {
        "username": "Jaguarking",
        "name": "Jorge",
        "surname": "vivas",
        "email": "jvivas@unemi.edu.ec",
        "age": 30,
        "password": crypt.hash("$2a$12$7NTHs2k1347iRrKSm.TZZ.uYqYC4yJpH5Lyt5XqF4HPilXNi2y9Xu"),
        "disabled": True
    }
}
def search_user_db(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    return None

async def auth_user(token=str=Depends(oauth2_scheme)):
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMS]).get("sub")
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

async def current_users(users:users=Depends(auth_user)):
    user = search_user(users)
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
     user_db = search_user_db(form_data.username)
     if not user_db:
         raise HTTPException(
            status_code=400, detail="Incorrect username or password")
user= search_user(form.username)

if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")


access_token={"sub": user.username,
              "exp": datetime.utcnow() + timedelta(minutes=Access_TOKEN_DURATION) }
        
return{"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHMS[0]), "token_type": "bearer"}



