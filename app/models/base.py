import uuid

from sqlalchemy import Boolean, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class EntityBase(Base):
    __abstract__ = True  # This class will NOT create a table

    id = Column(UUID(as_uuid=True),  primary_key=True, default=uuid.uuid4)
    is_deleted = Column(Boolean, default=False, nullable=False)