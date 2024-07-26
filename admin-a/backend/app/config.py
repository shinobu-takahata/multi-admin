from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    sqlalchemy_database_url: str
    secret_key: str
    cognito_region: str
    cognito_pool_id: str
    cognito_app_client_id: str
    cognito_app_client_secret: str
    # ALGORITHM: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int
    # REFRESH_TOKEN_EXPIRE_MINUTES: int


@lru_cache()
def get_settings():
    return Settings()
