from datetime import datetime
from fastapi_filter.contrib.sqlalchemy import Filter

from typing import Optional

from pydantic import Field
from database.models import Task


class TaskFilter(Filter):
    title__like: Optional[list[str]] = Field(alias="titles")
    created_at__gte: Optional[str] = Field(alias="created_at")

    class Constants(Filter.Constants):
        model = Task

    class Config:
        populate_by_name = True
