from database.models.user.auth import Auth
from database.services.CRUD import BaseCRUD
from database.base import get_session
from sqlalchemy import select, and_


class AuthService(BaseCRUD):

    def __init__(self):
        super(AuthService, self).__init__(Auth, Auth.auth_id.key)

    async def get(self, auth_id: int = None, user_id: int = None, refresh_token: str = None) -> Auth:
        async with get_session() as session:
            if auth_id:
                stmt = await session.execute(select(Auth).where(Auth.auth_id == auth_id))
            elif user_id:
                stmt = await session.execute(select(Auth).where(and_(Auth.user_id == user_id, Auth.denied == False)))
            elif refresh_token:
                stmt = await session.execute(select(Auth).where(Auth.refresh_token == refresh_token))
            return stmt.scalars().first()

    async def update(self, refresh_token: str, auth_id: int = None, user_id: int = None) -> Auth:
        if auth_id is None and user_id is None:
            return None

        async with get_session() as session:
            if auth_id:
                stmt = await session.execute(select(Auth).where(Auth.auth_id == auth_id))
            elif user_id:
                stmt = await session.execute(select(Auth).where(Auth.user_id == user_id))

            if not stmt:
                return None

            obj = stmt.scalars().first()
            if obj:
                obj.refresh_token = refresh_token
                await session.commit()
                await session.refresh(obj)
                return obj

    async def mark_denied(self, auth_id: int = None, refresh_token: str = None) -> Auth:
        async with get_session() as session:
            if auth_id:
                stmt = select(Auth).where(Auth.auth_id == auth_id)
            elif refresh_token:
                stmt = select(Auth).where(Auth.refresh_token == refresh_token)

            result = await session.execute(stmt)
            obj = result.scalars().first()
            if obj:
                obj.denied = True
                await session.flush()
                return obj
