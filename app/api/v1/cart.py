from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.db.deps import get_db
from app.models.cart import Cart, CartItem
from app.models.menu import MenuItem
from app.schemas.cart import CartItemCreate, CartOut
from app.core.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

# Utility: get or create cart

def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.post("/items", response_model=CartOut)
def add_to_cart(
    item_in: CartItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    menu_item = db.query(MenuItem).filter(MenuItem.id == item_in.menu_item_id).first()
    if not menu_item or not menu_item.is_available:
        raise HTTPException(status_code=404, detail="Menu item not available")

    cart = get_or_create_cart(db, current_user.id)

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.menu_item_id == menu_item.id)
        .first()
    )


    if cart_item:
        cart_item.quantity += item_in.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            menu_item_id=menu_item.id,
            quantity=item_in.quantity,
            price=menu_item.price,
        )
        db.add(cart_item)

# Recalculate total
    cart.total_amount = sum(i.quantity * i.price for i in cart.items)

    db.commit()
    db.refresh(cart)
    return cart

@router.get("/", response_model=CartOut)
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart is empty")
    return cart


@router.delete("/items/{cart_item_id}", response_model=CartOut)
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")


    item = (
        db.query(CartItem)
        .filter(CartItem.id == cart_item_id, CartItem.cart_id == cart.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(item)

    # Recalculate total
    cart.total_amount = sum(i.quantity * i.price for i in cart.items if i.id != item.id)

    db.commit()
    db.refresh(cart)
    return cart