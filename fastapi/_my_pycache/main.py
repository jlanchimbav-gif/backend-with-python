

from fastapi import FastAPI
from routers import items

APP.include_routers(items.routers) # type: ignore
APP= FastAPI()

@APP.get("/")
def read_root():
    return {"Hello": "World"}