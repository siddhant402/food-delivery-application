from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, asc, desc

from app.db.deps import get_db
from app.models.restaurant import Restaurant
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantOut,
    RestaurantListResponse,
)
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


MAX_LIMIT = 50


@router.get("/discover", response_model=RestaurantListResponse)
def discover_restaurants(
        city: str = Query(..., min_length=2),
        locality: str | None = Query(None),
        pincode: str | None = Query(None),

        limit: int = Query(20, ge=1, le=MAX_LIMIT),
        offset: int = Query(0, ge=0),

        sort_by: str = Query("name"),
        order: str = Query("asc"),

        db: Session = Depends(get_db),
):
    # Validation
    if not locality and not pincode:
        raise HTTPException(
            status_code=400,
            detail="Either locality or pincode must be provided",
        )

    query = db.query(Restaurant).filter(
        Restaurant.city == city,
        Restaurant.is_active == True,
    )

    if locality and pincode:
        query = query.filter(
            or_(
                Restaurant.locality == locality,
                Restaurant.pincode == pincode,
            )
        )
    elif locality:
        query = query.filter(Restaurant.locality == locality)
    elif pincode:
        query = query.filter(Restaurant.pincode == pincode)

    # Sorting
    if sort_by == "name":
        sort_column = Restaurant.name
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field",
        )

    if order == "asc":
        query = query.order_by(
            asc(sort_column),
            asc(Restaurant.id),
        )
    else:
        query = query.order_by(
            desc(sort_column),
            desc(Restaurant.id),
        )

    # Compute total count BEFORE pagination
    total_count = query.count()

    # Apply pagination
    items = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total_count": total_count,
        "items": items,
    }
