from database.services.cart import CartItemService, CartService
from database.services.order import OrderService
from database.services.products import ProductCategoryService, ProductService
from database.services.user import RoleService, UserService, AuthService


class ServiceManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.role = RoleService()
        self.user = UserService()
        self.auth = AuthService()

        self.product_category = ProductCategoryService()
        self.product = ProductService()

        self.cart = CartService(self)
        self.cart_item = CartItemService()

        self.order = OrderService()
