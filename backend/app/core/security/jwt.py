import datetime
import uuid

import jwt
from app.core.config import AppSettings
from app.custom_exceptions.jwt_decode_exception import JwtDecodeException

settings = AppSettings()

jwt_secret_key = settings.jwt_secret_key.get_secret_value()
algorithm = settings.jwt_algorithm


def create_access_token(admin_user_id: int, admin_school_id: int) -> str:
    issue_time = datetime.datetime.now(datetime.timezone.utc)
    expire_time = issue_time + datetime.timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(admin_user_id),
        "school_id": str(admin_school_id),
        "iat": issue_time,
        "exp": expire_time,
        "jti": str(uuid.uuid4()),
    }

    token = jwt.encode(
        payload,
        jwt_secret_key,
        algorithm=algorithm,
    )

    return token


def decode_access_token(token: str) -> dict:
    try:
        decoded_payload = jwt.decode(token, jwt_secret_key, algorithms=[algorithm])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise JwtDecodeException("Token has expired")
    except jwt.InvalidTokenError:
        raise JwtDecodeException("Invalid token")
