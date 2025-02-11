from sqlalchemy import select
from sqlalchemy.orm import joinedload

from filters import TaskFilter
from dao.base import BaseDAO
from database.database import sessionmanager
from database.models import Task


class TasksDAO(BaseDAO):
    model = Task

    @classmethod
    async def find_one_by_id_and_user(cls, task_id: int, user_id: int):
        async with sessionmanager.session() as session:
            query = (
                select(cls.model)
                .where(cls.model.owner_id == user_id, cls.model.id == task_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def delete(cls, task_id: int):
        async with sessionmanager.session() as session:
            obj = select(cls.model).where(cls.model.id == task_id)
            result = await session.execute(obj)
            obj = result.scalar_one_or_none()
            await session.delete(obj)
            await session.commit()
            return

    @classmethod
    async def update(cls, updarted_task: dict, task_id: int):
        async with sessionmanager.session() as session:
            obj = select(cls.model).where(cls.model.id == task_id)
            result = await session.execute(obj)
            db_task = result.scalar_one_or_none()
            print(type(db_task))
            for key, value in updarted_task.items():
                setattr(db_task, key, value)
            await session.commit()
            await session.refresh(db_task)
            return db_task

    @classmethod
    async def find_all_by_user(cls, user_id: int, filter: TaskFilter):
        async with sessionmanager.session() as session:
            query = select(cls.model).where(cls.model.owner_id == user_id)
            if filter:
                query = filter.filter(query)
                query = filter.sort(query)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_by_title_and_user(cls, title: str, owner_id: int):
        async with sessionmanager.session() as session:
            query = (
                select(cls.model)
                .filter_by(owner_id=owner_id)
                .filter_by(title=title)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
