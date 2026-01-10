from sqlalchemy import Column, Integer, ForeignKey, Float, String
from app.db.base import Base
from app.core.payment_status import PaymentStatus


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    amount = Column(Float, nullable=False)
    provider = Column(String, nullable=False)  # razorpay / stripe
    status = Column(String, default=PaymentStatus.CREATED.value)
    provider_payment_id = Column(String, nullable=True)
