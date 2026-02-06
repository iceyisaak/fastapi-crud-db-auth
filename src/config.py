from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    DATABASE_URL: str
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


Config = Settings.model_validate({})  
print(f"DATABASE_URL loaded: {Config.DATABASE_URL}")