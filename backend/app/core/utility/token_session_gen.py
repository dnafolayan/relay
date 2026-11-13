import datetime

from app.core.config import settings
from app.core.redis import redis_client as r


async def generate_session(
    session_id: str, token_hash: str, user_id: int, school_id: int
):
    key: str = f"refresh_session:{session_id}"
    data: dict[str, int | str] = {
        "user_id": user_id,
        "school_id": school_id,
        "current_token_hash": token_hash,
        "status": "active",
    }

    expiration_seconds: int = int(
        datetime.timedelta(days=settings.refresh_token_expire_days).total_seconds()
    )

    await r.hset(key, mapping=data)
    await r.expire(key, expiration_seconds)
