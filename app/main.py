from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.protected import router as protected_router
from app.api.v1.restaurants import router as restaurant_router
from app.api.v1.menu import router as menu_router
from app.api.v1.public import router as public_router


app = FastAPI(title="Food Delivery Application")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(protected_router, prefix="/api/v1")
app.include_router(restaurant_router, prefix="/api/v1")
app.include_router(menu_router, prefix="/api/v1")
app.include_router(public_router, prefix="/api/v1")
@app.get("/api/v1/health")
def health_check():
    return {"status": "OK"}





