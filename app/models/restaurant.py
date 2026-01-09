from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Restaurant(Base):
    __tablename__ = "restaurants"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)


    is_approved = Column(Boolean, default=False)
    is_open = Column(Boolean, default=False)


    owner = relationship("User", backref="restaurants")