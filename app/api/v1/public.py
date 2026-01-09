from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.db.deps import get_db
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.schemas.public import PublicRestaurantOut, PublicMenuItemOut


router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/restaurants", response_model=list[PublicRestaurantOut])
def list_restaurants(db: Session = Depends(get_db)):
    return (
        db.query(Restaurant)
        .filter(Restaurant.is_approved == True, Restaurant.is_open == True)
        .all()
    )


@router.get("/restaurants/{restaurant_id}/menu", response_model=list[PublicMenuItemOut])
def get_public_menu(restaurant_id: int, db: Session = Depends(get_db)):
    return (
        db.query(MenuItem)
        .filter(
            MenuItem.restaurant_id == restaurant_id,
            MenuItem.is_available == True,
        )
        .all()
    )