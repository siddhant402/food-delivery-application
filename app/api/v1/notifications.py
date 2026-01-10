from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.notification import NotificationOut
from app.models.notification import Notification
from app.core.auth import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=list[NotificationOut])
def get_my_notifications(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    return (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.id.desc())
        .all()
    )
