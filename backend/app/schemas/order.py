from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderType, OrderStatus

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: str
    order_type: OrderType = OrderType.IMMEDIATE
    scheduled_for: Optional[datetime] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdateStatus(BaseModel):
    status: OrderStatus

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    status: OrderStatus
    total_amount: float
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)