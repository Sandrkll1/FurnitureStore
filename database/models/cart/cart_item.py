from sqlalchemy import BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database.base import Base


class CartItem(Base):
    __tablename__ = "CartItem"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cart_id = Column(BigInteger, ForeignKey("Cart.id"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("Product.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items", lazy="joined")
