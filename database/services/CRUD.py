from typing import Any, Type

from sqlalchemy import select

from database.base import get_session


class BaseCRUD:
    def __init__(self, model_class: Type, primary_key: str):
        self.model_class = model_class
        self.primary_key = primary_key

    async def create(self, **kwargs) -> Any:
        async with get_session() as session:
            obj = self.model_class(**kwargs)
            session.add(obj)
            await session.flush()
            await session.refresh(obj)
            return obj

    async def get(self, primary_key_value: int) -> Any:
        async with get_session() as session:
            result = await session.execute(
                select(self.model_class).where(
                    getattr(self.model_class, self.primary_key) == primary_key_value
                )
            )
            return result.scalars().first()

    async def update(
        self, primary_key_value: int, new_data: dict = None, **kwargs
    ) -> Any:
        new_data = kwargs if new_data is None else new_data
        async with get_session() as session:
            stmt = await session.execute(
                select(self.model_class).where(
                    getattr(self.model_class, self.primary_key) == primary_key_value
                )
            )
            obj = stmt.scalars().first()
            if obj:
                for key, value in new_data.items():
                    setattr(obj, key, value)
                await session.flush()
                await session.refresh(obj)
                return obj

    async def delete(self, primary_key_value: int) -> bool:
        async with get_session() as session:
            query = select(self.model_class).where(
                getattr(self.model_class, self.primary_key) == primary_key_value
            )
            result = await session.execute(query)
            obj = result.scalars().first()
            if obj:
                await session.delete(obj)
                return True
            return False
