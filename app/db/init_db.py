from app.db.session import engine
from app.db.base import Base

from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.notification import Notification
from app.models.payment import Payment

Base.metadata.create_all(bind=engine)
