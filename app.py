"""Main FastAPI Application Entry Point"""
import sys
import os

# Add the fastapi/_my_pycache directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fastapi/_my_pycache"))

# Import the app from main.py
from main import app

# Import auth routers
from basic_auth_users import router as basic_auth_router
from jwt_auth_user import router as jwt_router

# Include auth routers
app.include_router(basic_auth_router, prefix="/auth", tags=["basic-authentication"])
app.include_router(jwt_router, tags=["jwt-authentication"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
