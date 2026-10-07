from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # app settings
    app_name: str = "Relay API"
    app_description: str = "API for handling relay operations"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
