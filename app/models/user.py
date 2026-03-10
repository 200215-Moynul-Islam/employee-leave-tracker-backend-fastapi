from sqlalchemy import Column, String
from .base import EntityBase
from sqlalchemy.orm import relationship
from .leave_request import LeaveRequest


class User(EntityBase):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    leave_requests = relationship("LeaveRequest", back_populates="user")