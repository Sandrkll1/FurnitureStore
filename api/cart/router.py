from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from api.cart.schemas import (AddProduct, CartItemResponse, CartResponse,
                              OrderCreateRequest, OrderResponse)
from api.dependencies import get_current_user, get_service_manager, get_current_admin
from api.products.schemas import ProductResponse
from database.models.user import User
from database.service_manager import ServiceManager

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=CartResponse)
async def get_cart(
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager),
):
    cart = await manager.cart.get_cart_by_user_id(user.user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart is empty")

    items = [
        CartItemResponse(
            product_id=item.product_id,
            product_name=item.product.name,
            quantity=item.quantity,
            price=item.product.price,
            product=ProductResponse.model_validate(item.product, from_attributes=True)
        )
        for item in cart.items
    ]

    return CartResponse(items=items, total_price=sum([item.price for item in items]))


@router.post("/", status_code=status.HTTP_200_OK)
async def add_item_to_cart(
        add_product: AddProduct,
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager),
):
    product = await manager.product.get(add_product.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    await manager.cart.add_item_to_cart(user.user_id, add_product.product_id, add_product.quantity)
    return {"message": "Product added to cart successfully"}


@router.delete("/", status_code=status.HTTP_200_OK)
async def remove_item_from_cart(
        product_id: int,
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager),
):
    await manager.cart.remove_item_from_cart(user.user_id, product_id)
    return {"message": "Product removed from car successfully"}


@router.put("/", status_code=status.HTTP_200_OK)
async def update_item_quantity(
        product: AddProduct,
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager),
):
    if product.quantity < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The quantity cannot be negative")
    await manager.cart.update_item_quantity(user.user_id, product.product_id, product.quantity)
    return {"message": "Quantity of product updated successfully"}


@router.post("/order", response_model=OrderResponse)
async def create_order(
        order_request: OrderCreateRequest,
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager),
):
    cart = await manager.cart.get_cart_by_user_id(user.user_id)
    if not cart or not cart.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

    _total_price = getattr(cart, 'total_price', None)
    if not _total_price:
        _total_price = sum(item.quantity * item.product.price for item in cart.items)

    order = await manager.order.create(
        user_id=user.user_id,
        delivery_address=order_request.delivery_address,
        total_price=_total_price
    )

    await manager.order.add_order_items(order.id, cart.items)
    await manager.cart.deactivate_cart(cart.id)

    return OrderResponse.model_validate(order, from_attributes=True)


@router.get("/order/history")
@cache(expire=20)
async def get_order_history(
        limit: int = 10,
        offset: int = 0,
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager)
):
    return [
        OrderResponse.model_validate(order, from_attributes=True)
        for order in await manager.order.get_order_history(user.user_id, limit, offset)
    ]


@router.get("/order/{order_id}")
@cache(expire=30)
async def get_order_details(
        order_id: int,
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager)
):
    order = await manager.order.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.user_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return OrderResponse.model_validate(order, from_attributes=True)


@router.put("/order/{order_id}")
async def update_order_status(
    order_id: int,
    order_status: str,
    admin=Depends(get_current_admin),
    manager: ServiceManager = Depends(get_service_manager),
):
    """Обновить статус заказа"""
    order = await manager.order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await manager.order.update(order_id, new_data={"status": order_status})
    return {"message": "Order status updated successfully"}
