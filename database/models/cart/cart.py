from datetime import datetime

from sqlalchemy import TIMESTAMP, BigInteger, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class Cart(Base):
    __tablename__ = "Cart"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("User.user_id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan", lazy="joined")
