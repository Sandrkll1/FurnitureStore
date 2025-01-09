import enum
from datetime import datetime

from sqlalchemy import (TIMESTAMP, BigInteger, Column, Enum, Float, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship

from database.base import Base


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = 'Order'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("User.user_id"), nullable=False)

    delivery_address = Column(String, nullable=True)
    total_price = Column(Float, nullable=False, default=0)
    status = Column(String, Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING.value)

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="joined")
