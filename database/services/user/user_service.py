from sqlalchemy import func, select

from database.base import get_session
from database.models.user import User
from database.services.CRUD import BaseCRUD


class UserService(BaseCRUD):
    def __init__(self):
        super(UserService, self).__init__(User, User.user_id.key)

    async def get(self, user_id: int = None, email: str = None) -> User:
        async with get_session() as session:
            if user_id:
                result = await session.execute(select(User).where(User.user_id == user_id))
                return result.scalars().first()
            elif email:
                result = await session.execute(select(User).where(User.email == email))
                return result.scalars().first()

    async def get_total_users_count(self):
        async with get_session() as session:
            result = await session.execute(select(func.count(User.user_id)))
            return result.scalar_one()
