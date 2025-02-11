from datetime import date, datetime
from fastapi_filter.contrib.sqlalchemy import Filter

from database.models import Task


class TaskFilter(Filter):
    title__like: str | None = None
    created_at: datetime | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = Task
