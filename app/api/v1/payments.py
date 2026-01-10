from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.order import Order
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentOut
from app.core.auth import get_current_user
from app.core.payment_providers.factory import get_payment_provider
from app.core.payment_status import PaymentStatus

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create", response_model=PaymentOut)
def create_payment(
        payload: PaymentCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == payload.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your order")

    existing = db.query(Payment).filter(Payment.order_id == order.id).first()
    if existing:
        return existing

    provider = get_payment_provider(payload.provider)
    provider_payment_id = provider.create_payment(order.total_amount)

    payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        provider=payload.provider,
        provider_payment_id=provider_payment_id,
        status=PaymentStatus.CREATED.value,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
