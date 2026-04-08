from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str = None


router = APIRouter()

# In-memory database
products_list = [
    Product(id=1, name="Laptop", price=999.99, description="High-performance laptop"),
    Product(id=2, name="Mouse", price=29.99, description="Wireless mouse"),
    Product(id=3, name="Keyboard", price=79.99, description="Mechanical keyboard")
]


# Helper function
def search_product(product_id: int):
    product = next((p for p in products_list if p.id == product_id), None)
    return product


# Endpoints
@router.get("/products")
async def get_products():
    return products_list


@router.get("/products/{product_id}")
async def get_product(product_id: int):
    product = search_product(product_id)
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )


@router.get("/products/search/")
async def search_products_by_name(name: str):
    product = next((p for p in products_list if p.name.lower() == name.lower()), None)
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )


@router.post("/products/", status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    if search_product(product.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists"
        )
    products_list.append(product)
    return product


@router.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    for index, p in enumerate(products_list):
        if p.id == product_id:
            products_list[index] = product
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    for index, p in enumerate(products_list):
        if p.id == product_id:
            del products_list[index]
            return {"message": "Product deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )
