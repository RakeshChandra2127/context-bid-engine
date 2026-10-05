import json
import logging
from typing import Optional
import redis.asyncio as redis
from app.schemas import ContentAnalysis

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Optional[redis.Redis] = None
        self.hits = 0
        self.misses = 0

    async def connect(self) -> None:
        try:
            self.redis = redis.from_url(self.redis_url, decode_responses=True)
            await self.redis.ping()
            logger.info("Connected to Redis cache.")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis = None

    async def disconnect(self) -> None:
        if self.redis:
            await self.redis.close()
            logger.info("Disconnected from Redis cache.")

    async def get_analysis(self, content_hash: str) -> Optional[ContentAnalysis]:
        if not self.redis:
            self.misses += 1
            return None
            
        key = f"analysis:{content_hash}"
        try:
            data = await self.redis.get(key)
            if data:
                self.hits += 1
                return ContentAnalysis.model_validate_json(data)
            else:
                self.misses += 1
                return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            self.misses += 1
            return None

    async def set_analysis(self, content_hash: str, analysis: ContentAnalysis, ttl: int) -> None:
        if not self.redis:
            return
            
        key = f"analysis:{content_hash}"
        try:
            await self.redis.setex(key, ttl, analysis.model_dump_json())
        except Exception as e:
            logger.error(f"Redis set error: {e}")

    async def get_stats(self) -> dict:
        total = self.hits + self.misses
        hit_ratio = (self.hits / total) if total > 0 else 0.0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total_requests": total,
            "hit_ratio": hit_ratio
        }
