from fastapi import Query


def pagination_query(
        page: int = Query(0, alias="page"),
        limit: int = Query(10, alias="limit")
) -> tuple[int, int]:
    return page, limit
