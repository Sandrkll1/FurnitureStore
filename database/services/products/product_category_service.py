from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.base import get_session
from database.models.products import ProductCategory
from database.services.CRUD import BaseCRUD


class ProductCategoryService(BaseCRUD):
    def __init__(self):
        super(ProductCategoryService, self).__init__(
            ProductCategory, ProductCategory.id.key
        )

    async def get_all(self) -> list[ProductCategory]:
        async with get_session() as session:
            result = await session.execute(select(ProductCategory))
            return result.scalars().all()

    async def get_by_name(self, name: str) -> Optional[ProductCategory]:
        async with get_session() as session:
            result = await session.execute(
                select(ProductCategory).where(ProductCategory.name == name)
            )
            return result.scalar_one_or_none()
