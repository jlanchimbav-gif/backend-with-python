
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
import os

# Initialize FastAPI app
app = FastAPI()

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "STATICFILES")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return {"Hello": "World"}
