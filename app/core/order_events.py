from sqlalchemy.orm import Session
from app.core.notifications import create_notification
from app.core.email import send_email
from app.models.order import Order
from app.models.user import User


def notify_order_status_change(db: Session, order: Order):
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        return

    title = "Order Update"
    message = f"Your order #{order.id} is now {order.status}"

    # In-app notification
    create_notification(db, user.id, title, message)

    # Email notification
    send_email(
        to_email=user.email,
        subject="Order Status Updated",
        body=message,
    )
