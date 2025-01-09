from datetime import datetime

from sqlalchemy import (JSON, TIMESTAMP, BigInteger, Boolean, Column, Float,
                        ForeignKey, Integer, String)
from sqlalchemy.orm import relationship

from database.base import Base


class Product(Base):
    __tablename__ = "Product"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("ProductCategory.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False, default=0)
    media = Column(JSON, default=[])
    deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete")
