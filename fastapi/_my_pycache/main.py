
from fastapi import FastAPI 
from fastapi  import routers

APP= FastAPI()
APP.include_routers(routers)
APP= FastAPI()

@APP.get("/")
def read_root():
    return {"Hello": "World"}

