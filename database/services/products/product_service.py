from datetime import datetime
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from database.base import get_session
from database.models.products import Product, ProductCategory
from database.services.CRUD import BaseCRUD


class ProductService(BaseCRUD):
    def __init__(self):
        super(ProductService, self).__init__(Product, Product.id.key)

    async def create_product(
            self,
            category_id: int,
            name: str,
            description: str,
            price: float,
            media: list[str]
    ) -> Product:
        async with get_session() as session:
            product = Product(
                category_id=category_id,
                name=name,
                description=description,
                price=price,
                media=media
            )
            session.add(product)
            await session.flush()
            await session.commit()

            return product

    async def update_product(
            self,
            id: int,
            category_id: int,
            name: str,
            description: str,
            price: float,
            media: list[str]
    ) -> Product:
        async with get_session() as session:
            product = await session.get(Product, id)

            product.category_id = category_id
            product.name = name
            product.description = description
            product.price = price
            product.media = media if media is not None else product.media

            await session.commit()
            await session.refresh(product)

            return product

    async def get_products(
            self,
            category_id: int = None,
            limit: int = 50,
            offset: int = 0,
            search: str = None
    ) -> list[Product]:
        async with get_session() as session:
            query = select(Product).where(Product.deleted == False)

            if search:
                query = query.where(Product.name.ilike(f"%{search}%"))
            elif category_id:
                query = query.where(Product.category_id == category_id)

            result = await session.execute(
                query.limit(limit).offset(offset)
            )
            return result.unique().scalars().all()

    async def get_product_detail(self, product_id: int) -> Product:
        async with get_session() as session:
            result = await session.execute(
                select(Product).where(Product.id == product_id)
            )
            return result.scalars().first()

    async def get_new_products(self, limit: int = 10, offset: int = 10) -> list[Product]:
        async with get_session() as session:
            result = await session.execute(
                select(Product)
                .where(Product.deleted == False)
                .order_by(Product.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            return result.unique().scalars().all()

    async def get_products_by_category_ids(self, category_ids: list, exclude_product_ids: list, limit: int) -> list[
        Product]:
        async with get_session() as session:
            query = select(Product).where(
                Product.category_id.in_(category_ids),
                Product.id.notin_(exclude_product_ids),
                Product.deleted == False
            ).limit(limit)
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def get_popular_products(self, exclude_product_ids: list = [], limit: int = 10) -> list[Product]:
        async with get_session() as session:
            query = select(Product).where(
                Product.deleted == False,
                Product.id.notin_(exclude_product_ids)
            ).order_by(Product.total_views.desc()).limit(limit)
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def get_categories_by_product_ids(self, product_ids: list) -> list[ProductCategory]:
        async with get_session() as session:
            result = await session.execute(
                select(Product.category_id)
                .where(Product.id.in_(product_ids))
                .distinct()
            )
            category_ids = [row[0] for row in result.fetchall()]
            if not category_ids:
                return []
            categories_result = await session.execute(
                select(ProductCategory).where(ProductCategory.id.in_(category_ids))
            )
            return categories_result.unique().scalars().all()

    async def get_most_expensive(self, limit: int = 10) -> list[Product]:
        async with get_session() as session:
            query = select(Product).where(
                Product.deleted == False
            ).order_by(Product.price.desc()).limit(limit)
            result = await session.execute(query)
            return result.unique().scalars().all()
