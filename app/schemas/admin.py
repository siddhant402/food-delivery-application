from pydantic import BaseModel


class AdminUserOut(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool


class Config:
    from_attributes = True


class AdminRestaurantOut(BaseModel):
    id: int
    name: str
    address: str
    is_approved: bool
    is_open: bool


class Config:
    from_attributes = True


class AdminOrderOut(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    total_amount: float
    status: str


class Config:
    from_attributes = True
