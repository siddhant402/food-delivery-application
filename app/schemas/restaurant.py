from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    description: str | None = None

    address_line: str
    locality: str
    city: str
    state: str
    pincode: str


class RestaurantOut(BaseModel):
    id: int
    name: str
    description: str | None

    address_line: str
    locality: str
    city: str
    state: str
    pincode: str

    is_active: bool
    owner_id: int

    class Config:
        from_attributes = True


class Config:
    from_attributes = True
