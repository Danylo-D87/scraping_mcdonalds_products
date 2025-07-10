from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache



class Settings(BaseSettings):
    products_file_path: str = "products.json"

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


@lru_cache()
def get_settings():
    return Settings()
