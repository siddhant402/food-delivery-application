from pydantic import BaseModel


class CartItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1


class CartItemOut(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price: float


class Config:
    from_attributes = True


class CartOut(BaseModel):
    id: int
    total_amount: float
    items: list[CartItemOut]


class Config:
    from_attributes = True