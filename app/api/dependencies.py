from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.database import get_db
from app.services.cache_service import CacheService
from app.services.content_fetcher import ContentFetcher
from app.services.content_analyzer import ContentAnalyzer
from app.services.ad_selector import AdSelector
from app.config import get_settings

settings = get_settings()

_cache_service = None

async def get_redis_client() -> Redis:
    return Redis.from_url(settings.redis_url, decode_responses=True)

async def get_cache_service(redis: Redis = Depends(get_redis_client)) -> CacheService:
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService(redis)
    return _cache_service

def get_content_fetcher() -> ContentFetcher:
    return ContentFetcher()

def get_content_analyzer() -> ContentAnalyzer:
    return ContentAnalyzer()

def get_ad_selector(
    db: AsyncSession = Depends(get_db),
    cache: CacheService = Depends(get_cache_service),
    analyzer: ContentAnalyzer = Depends(get_content_analyzer),
    fetcher: ContentFetcher = Depends(get_content_fetcher)
) -> AdSelector:
    return AdSelector(db=db, cache=cache, analyzer=analyzer, fetcher=fetcher)
