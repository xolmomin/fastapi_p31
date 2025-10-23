from typing import Optional, Any, Dict, List

from sqlalchemy import select, func, or_, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession


async def apply_filters(query, model, filters: Dict[str, Any]):
    for field, value in filters.items():
        if value is not None and hasattr(model, field):
            query = query.where(getattr(model, field) == value)
    return query


async def apply_search(query, model, search: Optional[str], search_fields: List[str]):
    if search:
        conditions = [
            getattr(model, field).ilike(f"%{search}%")
            for field in search_fields
            if hasattr(model, field)
        ]
        if conditions:
            query = query.where(or_(*conditions))
    return query


async def apply_sort(query, model, sort_by: Optional[str], sort_dir: Optional[str]):
    if sort_by and hasattr(model, sort_by):
        direction = asc if sort_dir == "asc" else desc
        query = query.order_by(direction(getattr(model, sort_by)))
    return query


async def paginate(
        db: AsyncSession,
        model,
        page: int,
        limit: int,
        query,
):
    total_query = select(func.count(model.id))
    total = (await db.execute(total_query)).scalar()

    query = query.limit(limit).offset((page - 1) * limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": limit,
        "pages": (total + limit - 1) // limit,
        "items": items,
    }


async def paginate_filter_sort(
        db: AsyncSession,
        model,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
        search_fields: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_dir: Optional[str] = "asc",
):
    query = select(model)
    search_fields = search_fields or []
    filters = filters or {}

    query = await apply_filters(query, model, filters)
    query = await apply_search(query, model, search, search_fields)
    query = await apply_sort(query, model, sort_by, sort_dir)

    return await paginate(db, model, page, limit, query)
