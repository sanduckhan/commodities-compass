from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, commodities, dashboard, historical, audio

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(
    commodities.router, prefix="/commodities", tags=["commodities"]
)
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(historical.router, prefix="/historical", tags=["historical"])
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
