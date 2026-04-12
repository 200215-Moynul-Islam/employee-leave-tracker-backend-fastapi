from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Base, EntityBase


TBaseModel = TypeVar("TBaseModel", bound=Base)
TEntityBaseModel = TypeVar("TEntityBaseModel", bound=EntityBase)


class BaseRepository(Generic[TBaseModel]):
    def __init__(self, db: AsyncSession, model: type[TBaseModel]):
        self.db = db
        self.model = model

    async def commit(self) -> None:
        await self.db.commit()

    def create(self, instance: TBaseModel) -> None:
        self.db.add(instance)


class EntityBaseRepository(BaseRepository[TEntityBaseModel], Generic[TEntityBaseModel]):
    def __init__(self, db: AsyncSession, model: type[TEntityBaseModel]):
        super().__init__(db, model)

    async def get_all_active(self) -> list[TEntityBaseModel]:
        statement = select(self.model).where(self.model.is_deleted.is_(False))
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_active_by_id(self, entity_id) -> TEntityBaseModel | None:
        statement = select(self.model).where(self.model.is_deleted.is_(False), self.model.id == entity_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
