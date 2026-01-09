from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.order import Order
from app.schemas.order import OrderOut, OrderStatusUpdate
from app.core.auth import require_roles, get_current_user
from app.core.order_status import OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])

# Allowed transitions per role
ROLE_TRANSITIONS = {
    "RESTAURANT": {OrderStatus.PLACED: OrderStatus.ACCEPTED,
                   OrderStatus.ACCEPTED: OrderStatus.PREPARING},
    "DELIVERY": {OrderStatus.PREPARING: OrderStatus.PICKED_UP},
    "ADMIN": {
        OrderStatus.PLACED: OrderStatus.CANCELLED,
        OrderStatus.ACCEPTED: OrderStatus.CANCELLED,
    },
}


@router.post("/place", response_model=OrderOut)
def place_order(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # All items must belong to same restaurant
    restaurant_ids = {item.menu_item_id for item in cart.items}

    # Fetch restaurant_id from first menu item
    first_menu_item = cart.items[0]
    restaurant_id = db.execute(
        "SELECT restaurant_id FROM menu_items WHERE id = :id",
        {"id": first_menu_item.menu_item_id},
    ).scalar()

    order = Order(
        user_id=current_user.id,
        restaurant_id=restaurant_id,
        total_amount=cart.total_amount,
        status="PLACED",
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            price=item.price,
        )
    db.add(order_item)

    # Clear cart
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()

    db.commit()
    db.refresh(order)
    return order


@router.get("/my", response_model=list[OrderOut])
def get_my_orders(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()


@router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status(
        order_id: int,
        payload: OrderStatusUpdate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    user_role = current_user.role
    current_status = OrderStatus(order.status)
    new_status = payload.status

    allowed = ROLE_TRANSITIONS.get(user_role, {})
    if current_status not in allowed or allowed[current_status] != new_status:
        raise HTTPException(status_code=403, detail="Invalid status transition")

    order.status = new_status.value
    db.commit()
    db.refresh(order)
    return order


@router.get("/active", response_model=list[OrderOut])
def get_active_orders(
        db: Session = Depends(get_db),
        current_user=Depends(require_roles("RESTAURANT", "DELIVERY", "ADMIN")),
):
    return (
        db.query(Order)
        .filter(Order.status != OrderStatus.DELIVERED.value)
        .all()
    )
