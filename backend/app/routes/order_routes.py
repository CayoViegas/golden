from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdateStatus
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(db)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    service: OrderService = Depends(get_service)
):
    return service.create(order_in)

@router.get("/", response_model=List[OrderResponse])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    service: OrderService = Depends(get_service)
):
    return service.get_all(skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderResponse)
def read_order(
    order_id: int,
    service: OrderService = Depends(get_service)
):
    order = service.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_in: OrderUpdateStatus,
    service: OrderService = Depends(get_service)
):
    order = service.update_status(order_id, status_in)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order