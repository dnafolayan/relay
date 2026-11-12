from app.core.config import settings
from redis.asyncio import Redis

redis_client: Redis = Redis.from_url(
    settings.redis_url.get_secret_value(), decode_responses=True
)
