from pydantic import BaseModel

from api.products.schemas import ProductResponse


class AddProduct(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemResponse(AddProduct):
    product_name: str
    price: float
    product: ProductResponse


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total_price: float


class OrderCreateRequest(BaseModel):
    delivery_address: str


class OrderItemResponse(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float
    product: ProductResponse


class OrderResponse(OrderCreateRequest):
    id: int
    user_id: int
    status: str
    total_price: float
    items: list[OrderItemResponse]
