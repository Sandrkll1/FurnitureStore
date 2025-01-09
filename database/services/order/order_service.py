from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.base import get_session
from database.models.order import Order, OrderItem
from database.services.CRUD import BaseCRUD


class OrderService(BaseCRUD):
    def __init__(self):
        super(OrderService, self).__init__(Order, Order.id.key)

    async def add_order_items(self, order_id: int, cart_items: list):
        async with get_session() as session:
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.product.price
                )
                session.add(order_item)
            await session.commit()

    async def get_order_history(self, user_id: int, limit: int = 10, offset: int = 0) -> list[Order]:
        async with get_session() as session:
            query = select(Order).where(
                Order.user_id == user_id
            ).order_by(Order.id.desc()).offset(offset).limit(limit)
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def get_orders_by_user_id(self, user_id: int, status: str = None) -> list[Order]:
        async with get_session() as session:
            query = select(Order).where(Order.user_id == user_id)
            if status:
                query = query.where(Order.status == status)
            result = await session.execute(
                query.options(
                    selectinload(Order.items)
                )
            )
            return result.scalars().all()
