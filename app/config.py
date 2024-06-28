import os

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_user: str = os.getenv("POSTGRES_USER")
    db_password: str = os.getenv("POSTGRES_PASSWORD")
    db_host: str = os.getenv("POSTGRES_HOST")
    db_port: str = os.getenv("POSTGRES_PORT")
    db_name: str = os.getenv("POSTGRES_DB")
    db_url: str = (
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    redis_host: str = os.getenv("REDIS_HOST", "127.0.0.1")
    redis_port: str = os.getenv("REDIS_PORT", "6379")
    redis_url: str = f"redis://{redis_host}:{redis_port}"


database_settings = DatabaseSettings()
