from fastapi import Query
from app.core.config import settings


MINIMUM_VALUE = 0

def pagination_parameters(
    skip: int = Query(0, ge=MINIMUM_VALUE, description="The number of pages to skip"),
    limit: int = Query(settings.DEFAULT_ITEMS_PER_PAGE, le=settings.MAX_ITEMS_PER_PAGE, gt=MINIMUM_VALUE, description="The number of items to display per page")
):
    return {
        'skip': skip,
        'limit': limit
    }
