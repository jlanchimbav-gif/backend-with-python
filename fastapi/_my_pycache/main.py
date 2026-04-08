from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
from routers.users import router as users_router
from routers.products import router as products_router
import os

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(users_router, tags=["users"])
app.include_router(products_router, tags=["products"])

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "STATICFILES")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to FastAPI",
        "endpoints": {
            "/docs": "Swagger documentation",
            "/redoc": "ReDoc documentation",
            "/users": "List users",
            "/products": "List products",
            "/images": "Available images"
        }
    }

@app.get("/images")
def get_images():
    """Get available images from the images folder"""
    images_dir = os.path.join(os.path.dirname(__file__), "STATICFILES", "images")
    if os.path.exists(images_dir):
        images = os.listdir(images_dir)
        image_urls = [f"/static/images/{img}" for img in images]
        return {
            "total_images": len(images),
            "images": image_urls,
            "server_url": "http://localhost:8000"
        }
    return {"message": "No images directory found"}
