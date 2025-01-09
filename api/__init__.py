from fastapi import Depends, FastAPI

from api.auth import auth_router
from api.cart import cart_router
from api.dependencies import get_current_user
from api.products import product_router
from api.profile import user_router
from api.data import data_router


def setup(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(product_router)
    app.include_router(cart_router, dependencies=[Depends(get_current_user)])
    app.include_router(user_router)
    app.include_router(data_router)
