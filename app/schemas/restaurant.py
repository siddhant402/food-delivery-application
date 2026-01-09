from pydantic import BaseModel

class RestaurantCreate(BaseModel):
    name: str
    address: str


class RestaurantOut(BaseModel):
    id: int
    name: str
    address: str
    is_approved: bool
    is_open: bool


class Config:
    from_attributes = True