import time
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from redis.asyncio import Redis

from app.database import get_db
from app.api.dependencies import get_redis_client
from app.config import get_settings

router = APIRouter()
settings = get_settings()
start_time = time.time()

@router.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    uptime = int(time.time() - start_time)
    return {
        "status": "healthy",
        "version": settings.version,
        "uptime_seconds": uptime
    }

@router.get("/health/ready", tags=["Health"])
async def readiness_check(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis_client)
):
    """Deep readiness check including database and cache connectivity."""
    db_status = "unhealthy"
    redis_status = "unhealthy"
    
    try:
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        pass
        
    try:
        await redis.ping()
        redis_status = "healthy"
    except Exception:
        pass
        
    overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "unhealthy"
    
    return {
        "status": overall_status,
        "database": db_status,
        "redis": redis_status
    }
