from app.db.session import engine
from app.db.base import Base

from app.models.user import User
from app.models.restaurant import Restaurant

Base.metadata.create_all(bind=engine)