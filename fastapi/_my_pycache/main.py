
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
import os

# Initialize FastAPI app
app = FastAPI()

# Mount static files (optional - comment out if directory doesn't exist)
try:
    static_dir = os.path.join(os.path.dirname(__file__), "STATICFILES")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

@app.get("/")
def read_root():
    return {"Hello": "World"}
