from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class ProductCategory(Base):
    __tablename__ = "ProductCategory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("Product", cascade="all, delete")
