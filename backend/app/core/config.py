from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # app settings
    app_name: str = "Relay API"
    app_env: str = "development"
    app_description: str = "API for handling relay operations"

    db_url: SecretStr
    db_test_url: SecretStr

    jwt_secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=15, gt=0)
    refresh_token_expire_days: int = Field(default=7, gt=0)

    redis_url: SecretStr = SecretStr("redis://localhost:6379/0")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = AppSettings()
