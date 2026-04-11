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

    async def create(self, instance: TBaseModel) -> TBaseModel:
        self.db.add(instance)
        await self.db.commit()
        return instance


class EntityBaseRepository(BaseRepository[TEntityBaseModel], Generic[TEntityBaseModel]):
    def __init__(self, db: AsyncSession, model: type[TEntityBaseModel]):
        super().__init__(db, model)

    async def get_all_active(self) -> list[TEntityBaseModel]:
        statement = select(self.model).where(self.model.is_deleted.is_(False))
        result = await self.db.execute(statement)
        return list(result.scalars().all())
