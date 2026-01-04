from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

def get_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    service: ProductService = Depends(get_service)
):
    return service.create(product_in)

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    service: ProductService = Depends(get_service)
):
    return service.get_all(skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(
    product_id: int,
    service: ProductService = Depends(get_service)
):
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    service: ProductService = Depends(get_service)
):
    product = service.update(product_id, product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_service)
):
    success = service.delete(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None