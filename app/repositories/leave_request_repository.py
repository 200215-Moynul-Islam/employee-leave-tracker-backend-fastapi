from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import LeaveRequest
from app.repositories.base_repository import EntityBaseRepository


class LeaveRequestRepository(EntityBaseRepository[LeaveRequest]):
    def __init__(self, db):
        super().__init__(db, LeaveRequest)

    async def get_all_active_with_users(self) -> list[LeaveRequest]:
        statement = (
            select(self.model)
            .options(selectinload(self.model.user))
            .where(self.model.is_deleted.is_(False))
        )
        result = await self.db.execute(statement)

        return list(result.scalars().all())
