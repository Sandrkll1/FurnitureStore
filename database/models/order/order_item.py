from sqlalchemy import BigInteger, Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database.base import Base


class OrderItem(Base):
    __tablename__ = 'OrderItem'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("Order.id"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("Product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", lazy="joined")
