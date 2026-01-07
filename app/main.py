from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.protected import router as protected_router

app = FastAPI(title="Food Delivery Application")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(protected_router, prefix="/api/v1")
@app.get("/api/v1/health")
def health_check():
    return {"status": "OK"}





