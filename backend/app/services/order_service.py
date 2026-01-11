from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdateStatus


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_in: OrderCreate) -> Order:
        db_order = Order(
            customer_name=order_in.customer_name,
            customer_phone=order_in.customer_phone,
            customer_address=order_in.customer_address,
            order_type=order_in.order_type,
            scheduled_for=order_in.scheduled_for,
            status=OrderStatus.RECEIVED,
            total_amount=0.0,
        )
        self.db.add(db_order)
        self.db.flush()

        total = 0.0

        for item_in in order_in.items:
            product = self.db.get(Product, item_in.product_id)
            if not product:
                self.db.rollback()
                raise HTTPException(
                    status_code=404, detail=f"Product ID {item_in.product_id} not found"
                )

            item_total = product.price * item_in.quantity
            total += item_total

            db_item = OrderItem(
                order_id=db_order.id,
                product_id=item_in.product_id,
                quantity=item_in.quantity,
                unit_price=product.price,
            )
            self.db.add(db_item)

        db_order.total_amount = total
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        stmt = select(Order).offset(skip).limit(limit).order_by(Order.created_at.desc())
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self.db.get(Order, order_id)

    def update_status(
        self, order_id: int, status_in: OrderUpdateStatus
    ) -> Optional[Order]:
        db_order = self.get_by_id(order_id)
        if not db_order:
            return None

        db_order.status = status_in.status
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
