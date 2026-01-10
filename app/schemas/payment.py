from pydantic import BaseModel
from app.core.payment_status import PaymentStatus


class PaymentCreate(BaseModel):
    order_id: int
    provider: str  # razorpay / stripe


class PaymentOut(BaseModel):
    id: int
    order_id: int
    amount: float
    provider: str
    status: PaymentStatus


class Config:
    from_attributes = True
