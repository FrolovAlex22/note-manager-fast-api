from dao.base import BaseDAO
from database.database import sessionmanager
from database.models import User


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def add(cls, user_dict: dict):
        async with sessionmanager.session() as session:
            user = User(**user_dict)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
