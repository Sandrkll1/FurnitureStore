from copy import deepcopy

from sqlalchemy import and_, select, update
from sqlalchemy.orm import joinedload, selectinload

from database.base import get_session
from database.models.cart import Cart, CartItem
from database.models.user import User
from database.services.CRUD import BaseCRUD


class CartService(BaseCRUD):
    def __init__(self, manager):
        super(CartService, self).__init__(Cart, Cart.id.key)
        self.manager = manager

    async def get_cart_by_user_id(self, user_id: int) -> Cart:
        async with get_session() as session:
            result = await session.execute(
                select(Cart)
                .where(and_(Cart.user_id == user_id, Cart.is_active == True))
                .options(
                    selectinload(Cart.items).joinedload(CartItem.product)
                )
            )
            cart = result.scalars().first()
            if not cart:
                cart = Cart(user_id=user_id)
                session.add(cart)
                await session.commit()
                await session.refresh(cart)
            return cart

    async def add_item_to_cart(self, user_id: int, product_id: int, quantity: int = 1):
        async with get_session() as session:
            cart = await self.get_cart_by_user_id(user_id)
            item = next((item for item in cart.items if item.product_id == product_id), None)
            if item:
                item.quantity += quantity
            else:
                new_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
                session.add(new_item)
            await session.commit()

    async def remove_item_from_cart(self, user_id: int, product_id: int):
        async with get_session() as session:
            cart = await self.get_cart_by_user_id(user_id)
            item = next((item for item in cart.items if item.product_id == product_id), None)
            if item:
                await session.delete(item)
                await session.commit()

    async def update_item_quantity(self, user_id: int, product_id: int, quantity: int):
        async with get_session() as session:
            cart = await self.get_cart_by_user_id(user_id)
            item = next((item for item in cart.items if item.product_id == product_id), None)

            if item:
                if quantity > 0:
                    await session.execute(
                        update(CartItem)
                        .where(CartItem.id == item.id)
                        .values(quantity=quantity)
                    )
                else:
                    await session.delete(item)
                await session.commit()
            else:
                if quantity > 0:
                    new_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
                    session.add(new_item)
                    await session.commit()

    async def deactivate_cart(self, cart_id: int):
        await self.update(cart_id, is_active=False)
