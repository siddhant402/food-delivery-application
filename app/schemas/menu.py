from pydantic import BaseModel


class MenuCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class MenuOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    is_available: bool

    class Config:
        from_attributes = True