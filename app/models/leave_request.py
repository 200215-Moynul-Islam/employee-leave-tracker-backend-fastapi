from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import EntityBase


class LeaveRequest(EntityBase):
    __tablename__ = "leave_requests"

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(Date, nullable=False)
    status = Column(String, nullable=False)

    user_id = Column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="leave_requests")