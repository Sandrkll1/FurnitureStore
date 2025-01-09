from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class Auth(Base):
    __tablename__ = 'Auth'

    auth_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    refresh_token = Column(Text)
    denied = Column(Boolean, default=False)

    user = relationship("User", back_populates="auth")
