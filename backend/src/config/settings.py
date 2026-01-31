from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str
    better_auth_secret: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


# Load settings
settings = Settings()