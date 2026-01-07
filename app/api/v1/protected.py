from fastapi import APIRouter, Depends
from app.core.auth import require_roles

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/customer")
def customer_endpoint(user=Depends(require_roles("CUSTOMER"))):
    return {"message": "Customer access granted"}


@router.get("/admin")
def admin_endpoint(user=Depends(require_roles("ADMIN"))):
    return {"message": "Admin access granted"}