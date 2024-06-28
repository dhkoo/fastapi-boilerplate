import os

from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    db_user: str = os.environ.get("POSTGRES_USER", "postgres")
    db_password: str = os.environ.get("POSTGRES_PASSWORD", "postgres-password")
    db_host: str = os.environ.get("POSTGRES_HOST", "127.0.0.1")
    db_port: str = os.environ.get("POSTGRES_PORT", "5434")
    db_name: str = os.environ.get("POSTGRES_DB", "project")
    db_url: str = (
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    redis_host: str = os.environ.get("REDIS_HOST", "127.0.0.1")
    redis_port: str = os.environ.get("REDIS_PORT", "6379")
    redis_url: str = f"redis://{redis_host}:{redis_port}"
