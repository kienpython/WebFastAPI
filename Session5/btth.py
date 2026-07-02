from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {"id": 1, "name": "Keyboard", "price": 500000},
    {"id": 2, "name": "Mouse", "price": 300000}
]


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)


@app.get("/products")
def get_products():
    return {
        "message": "Get products successfully",
        "data": products
    }


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    new_id = max(item["id"] for item in products) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price
    }

    products.append(new_product)

    return {
        "message": "Create product successfully",
        "data": new_product
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {
                "message": "Delete product successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )