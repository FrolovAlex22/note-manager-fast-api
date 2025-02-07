from sqlalchemy.future import select
from database.database import sessionmanager


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, add_dict: dict):
        async with sessionmanager.session() as session:
            obj = cls.model(**add_dict)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @classmethod
    async def find_all(cls):
        async with sessionmanager.session() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, obj_id: int):
        async with sessionmanager.session() as session:
            query = select(cls.model).filter_by(id=obj_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
