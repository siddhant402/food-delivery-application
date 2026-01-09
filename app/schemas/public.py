from pydantic import BaseModel

class PublicRestaurantOut(BaseModel):
    id: int
    name: str
    address: str
    is_open: bool

class Config:
    from_attributes = True

class PublicMenuItemOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: float

class Config:
    from_attributes = True