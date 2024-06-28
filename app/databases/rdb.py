from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import database_settings

print(database_settings.db_url)
engine = create_async_engine(database_settings.db_url)

async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db():
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
