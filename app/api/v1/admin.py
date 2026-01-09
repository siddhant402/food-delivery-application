from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.order import Order
from app.schemas.admin import AdminUserOut, AdminRestaurantOut, AdminOrderOut
from app.core.auth import require_roles

router = APIRouter(prefix="/admin", tags=["Admin"])


# USERS
@router.get("/users", response_model=list[AdminUserOut])
def list_users(
        db: Session = Depends(get_db),
        current_user=Depends(require_roles("ADMIN"))
):
    return db.query(User).all()


@router.put("/users/{user_id}/deactivate", response_model=AdminUserOut)
def deactivate_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(require_roles("ADMIN"))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


# RESTAURANTS
@router.get("/restaurants", response_model=list[AdminRestaurantOut])
def list_restaurants(
        db: Session = Depends(get_db),
        current_user=Depends(require_roles("ADMIN"))
):
    return db.query(Restaurant).all()


@router.put("/restaurants/{restaurant_id}/toggle", response_model=AdminRestaurantOut)
def toggle_restaurant(
        restaurant_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(require_roles("ADMIN"))
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    restaurant.is_open = not restaurant.is_open
    db.commit()
    db.refresh(restaurant)
    return restaurant


# ---------------- ORDERS ----------------

@router.get("/orders", response_model=list[AdminOrderOut])
def list_orders(
        db: Session = Depends(get_db),
        current_user=Depends(require_roles("ADMIN"))
):
    return db.query(Order).all()
