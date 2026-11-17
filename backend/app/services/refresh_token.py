import hashlib

from app.core.redis import redis_client as r


async def rotate_refresh_token(refresh_token: str) -> tuple[str, str]:
    session_id, secret = refresh_token.split(".", 1)
    token_hash: str = hashlib.sha256(secret.encode("utf-8")).hexdigest()
