
from fastapi import FastAPI 

  ## routers ##
from fastapi._my_pycache import app
from fastapi._my_pycache.routers import products
from fastapi._my_pycache.routers.users import users 
from fastapi.staticfiles import StaticFiles
APP= FastAPI()
APP.include_routers(products.router)
APP.include_routers(users.router)
APP= FastAPI()

## mount ##
app.mount("/static", StaticFiles(directory="static"), name="static")

@APP.get("/")
def read_root():
    return {"Hello": "World"}
