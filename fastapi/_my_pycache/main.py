from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from routers.users import router as users_router
import os

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(users_router, tags=["users"])

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "STATICFILES")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI", "endpoints": {"/api/docs": "Swagger documentation", "/api/redoc": "ReDoc documentation", "/users": "List users"}}
