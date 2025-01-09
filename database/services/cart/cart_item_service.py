from database.models.cart import CartItem
from database.services.CRUD import BaseCRUD


class CartItemService(BaseCRUD):
    def __init__(self):
        super(CartItemService, self).__init__(CartItem, CartItem.id.key)
