from sqlalchemy import select
from dao.base import BaseDAO
from database.database import sessionmanager
from database.models import User


class UsersDAO(BaseDAO):
    model = User


    @classmethod
    async def find_one_or_none_by_name(cls, username: str):
        async with sessionmanager.session() as session:
            query = select(cls.model).filter_by(username=username)
            result = await session.execute(query)
            return result.scalar_one_or_none()
