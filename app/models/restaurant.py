from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.base import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    __table_args__ = (
        Index("idx_city", "city"),
        Index("idx_locality", "locality"),
        Index("idx_pincode", "pincode"),
        Index("idx_is_active", "is_active"),
    )

    id = Column(Integer, primary_key=True, index=True)

    # Identity
    name = Column(String, nullable=False)  # Restaurant name
    description = Column(String, nullable=True)

    # Address (normalized)
    address_line = Column(String, nullable=False)  # Street / building
    locality = Column(String, nullable=False)  # Area (HSR Layout)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    pincode = Column(String, nullable=False)

    is_active = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
