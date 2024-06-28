from fastapi import Query
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import database_settings

db_config = database_settings

engine = create_async_engine(db_config.db_url)
sync_engine = create_engine(db_config.db_sync_url)


async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
sync_session = sessionmaker(
    autocommit=False, autoflush=False, bind=sync_engine)


Base = declarative_base()


async def get_db():
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


def get_sync_db():
    db = sync_session()
    return db
