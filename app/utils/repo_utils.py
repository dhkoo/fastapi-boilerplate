from typing import Any, Optional, Type
from urllib.parse import urlparse
from fastapi import HTTPException
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


def apply_filters(query, model_type: Type[Any], filters: dict):
    for field, value in filters.items():
        query = query.where(getattr(model_type, field) == value)
    return query


def is_valid_url(value):
    try:
        result = urlparse(str(value))
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


async def handle_db_error(operation):
    try:
        return await operation()
    except SQLAlchemyError as e:
        print(f"Error occurred: {e}")
        return None


async def get_mapped_result(db, query):
    async def operation():
        record = await db.execute(query)
        return record.mappings().first() if record else None
    return await handle_db_error(operation)


async def get_mapped_results(db, query, page, limit):
    async def operation():
        records = await db.execute(query.offset(page * limit).limit(limit))
        return records.mappings().all() if records else []
    return await handle_db_error(operation)


async def get_mapped_all_results(db, query):
    async def operation():
        records = await db.execute(query)
        return records.mappings().all() if records else []
    return await handle_db_error(operation)


async def get_total_count(db, query):
    async def operation():
        total_query = select(func.count()).select_from(query.subquery())
        total_res = await db.execute(total_query)
        return total_res.scalar()
    return await handle_db_error(operation) or 0


async def get_record(db: AsyncSession, model_type: Type[Any], filters: dict):
    try:
        query = select(model_type)
        query = apply_filters(query, model_type, filters)
        res = await db.execute(query)
        return res.scalar()
    except SQLAlchemyError as e:
        return None


async def get_record_list(
    db: AsyncSession,
    model_type: Type[Any],
    page: int,
    limit: int,
    filters: Optional[dict] = None,
    join_table: Optional[Type[Any]] = None,
    sort_field: Optional[str] = None,
    sort_order: Optional[str] = None,
):
    query = select(model_type)

    if join_table:
        query = query.options(joinedload(join_table))

    if filters:
        query = apply_filters(query, model_type, filters)

    if sort_field:
        if sort_order == "desc":
            query = query.order_by(desc(sort_field))
        else:
            query = query.order_by(asc(sort_field))

    res = await db.execute(query.offset(page * limit).limit(limit))
    return res.scalars().all()


async def execute_db_operation(operation):
    try:
        return await operation()
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Integrity constraint violation.")
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


async def create_record(db: AsyncSession, model_type: Type[Any], data: dict):
    async def operation():
        new_record = model_type(**data)
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
        return new_record
    return await execute_db_operation(operation)


async def update_record(db: AsyncSession, record: Any, data: dict):
    async def operation():
        for key, value in data.items():
            if hasattr(record, key):
                setattr(record, key, value)
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record
    return await execute_db_operation(operation)


async def delete_record(db: AsyncSession, model_type: Type[Any], filters: Optional[dict] = None):
    async def operation():
        query = select(model_type)
        if filters:
            query = apply_filters(query, model_type, filters)
        records = await db.execute(query)
        records = records.scalars().all()
        for record in records:
            await db.delete(record)
        await db.commit()
        return {"message": f"Record(s) deleted successfully"}

    return await execute_db_operation(operation)
