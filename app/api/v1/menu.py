from fastapi import APIRouter, Depends, HTTPException
from app.models.restaurant import Restaurant
from app.schemas.menu import MenuCreate, MenuOut
from app.core.auth import require_roles
from app.db.deps import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix="/menu", tags=["Menu"])


@router.post("/restaurants/{restaurant_id}", response_model=MenuOut)
def add_menu_item(
    restaurant_id: int,
    menu_in: MenuCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("RESTAURANT")),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")


    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not restaurant owner")


    if not restaurant.is_approved:
        raise HTTPException(status_code=400, detail="Restaurant not approved")


    item = MenuItem(
        restaurant_id=restaurant_id,
        name=menu_in.name,
        description=menu_in.description,
        price=menu_in.price,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/restaurants/{restaurant_id}", response_model=list[MenuOut])
def get_menu_for_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(MenuItem)
        .filter(MenuItem.restaurant_id == restaurant_id, MenuItem.is_available == True)
        .all()
    )


@router.put("/{menu_id}/availability", response_model=MenuOut)
def toggle_menu_availability(
    menu_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("RESTAURANT")),
):
    item = db.query(MenuItem).filter(MenuItem.id == menu_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")


    restaurant = db.query(Restaurant).filter(Restaurant.id == item.restaurant_id).first()
    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not restaurant owner")


    item.is_available = not item.is_available
    db.commit()
    db.refresh(item)
    return item