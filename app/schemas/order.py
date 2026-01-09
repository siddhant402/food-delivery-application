from pydantic import BaseModel
from app.core.order_status import OrderStatus


class OrderItemOut(BaseModel):
    menu_item_id: int
    quantity: int
    price: float


class Config:
    from_attributes = True


class OrderOut(BaseModel):
    id: int
    restaurant_id: int
    total_amount: float
    status: str
    items: list[OrderItemOut]


class Config:
    from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
