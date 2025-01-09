import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class RoleEnum(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class Role(Base):
    __tablename__ = "Role"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, Enum(RoleEnum), nullable=False, unique=True, default=RoleEnum.USER.value)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="role")
