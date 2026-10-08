from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # app settings
    app_name: str = "Relay API"
    app_env: str = "development"
    app_description: str = "API for handling relay operations"

    db_url: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
