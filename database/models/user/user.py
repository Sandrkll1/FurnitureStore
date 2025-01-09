from datetime import datetime

from sqlalchemy import (TIMESTAMP, Column, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship

from database.base import Base


class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("Role.role_id"), nullable=False, default=1)

    name = Column(String(255), nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    birthday = Column(TIMESTAMP, nullable=True)
    image = Column(String, nullable=True)

    register_timestamp = Column(TIMESTAMP, default=datetime.utcnow)

    role = relationship("Role", back_populates="user", lazy="joined")
    auth = relationship("Auth", back_populates="user")

    carts = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")
