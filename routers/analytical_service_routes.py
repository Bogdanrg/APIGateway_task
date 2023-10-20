from fastapi import APIRouter

analytical_service_router = APIRouter(
    prefix="/api/analytical", tags=["analytical_service"]
)
