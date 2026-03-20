from fastapi import APIRouter, FastAPI
from fastapi._my_pycache import app

app = FastAPI()
router = APIRouter()

products_list = [{"product_1", "product_2", "product_3"}]

@router.get("/products/")
async def get_products():
    return products_list

@router.get("/products/{product_id}")
async def get_product(id: int):
       return products_list[id]
