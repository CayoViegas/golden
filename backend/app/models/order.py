from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .product import Product

# Enums
class OrderType(str, PyEnum):
    IMMEDIATE = "immediate"
    SCHEDULED = "scheduled"


class OrderStatus(str, PyEnum):
    RECEIVED = "received"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Customer Data
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    customer_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    customer_address: Mapped[str] = mapped_column(Text, nullable=False)

    # Order Meta
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    order_type: Mapped[OrderType] = mapped_column(Enum(OrderType), nullable=False)
    scheduled_for: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.RECEIVED
    )
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Keys
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    # Snapshot Data
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")
