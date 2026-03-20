
from fastapi import FastAPI 

  ## routers ##
from fastapi._my_pycache.routers import products
from fastapi._my_pycache.routers.users import users 

APP= FastAPI()
APP.include_routers(products.router)
APP.include_routers(users.router)
APP= FastAPI()

@APP.get("/")
def read_root():
    return {"Hello": "World"}

