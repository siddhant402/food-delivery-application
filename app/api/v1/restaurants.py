from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantOut
from app.core.auth import get_current_user, require_roles

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.post("/", response_model=RestaurantOut)
def create_restaurant(
        restaurant_in: RestaurantCreate,
        db: Session = Depends(get_db),
        current_user=Depends(require_roles("RESTAURANT")),
):
    restaurant = Restaurant(
        name=restaurant_in.name,
        description=restaurant_in.description,

        address_line=restaurant_in.address_line,
        locality=restaurant_in.locality,
        city=restaurant_in.city,
        state=restaurant_in.state,
        pincode=restaurant_in.pincode,

        owner_id=current_user.id,
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.get("/my", response_model=list[RestaurantOut])
def get_my_restaurants(
        db: Session = Depends(get_db),
        current_user=Depends(require_roles("RESTAURANT")),
):
    return db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()


@router.put("/{restaurant_id}/approve", response_model=RestaurantOut)
def approve_restaurant(
        restaurant_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(require_roles("ADMIN")),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    restaurant.is_approved = True
    restaurant.is_open = True
    db.commit()
    db.refresh(restaurant)
    return restaurant
