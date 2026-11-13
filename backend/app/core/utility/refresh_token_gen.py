import hashlib
import secrets
import uuid


def gen_refresh_token() -> tuple[str, str]:
    """Return (refresh_token, secret_hash)"""

    session_id: str = str(uuid.uuid4())
    secret: str = secrets.token_urlsafe(32)

    refresh_token: str = f"{session_id}.{secret}"

    secret_hash: str = hashlib.sha256(secret.encode("utf-8")).hexdigest()

    return (refresh_token, secret_hash)
