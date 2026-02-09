from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    DATABASE_URL: str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    REDIS_HOST:str="localhost"
    REDIS_PORT:int=6379
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


Config = Settings.model_validate({})  
print(f"DATABASE_URL loaded: {Config.DATABASE_URL}")