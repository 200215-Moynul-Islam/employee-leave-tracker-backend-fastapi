from sqlalchemy import select

from app.constants import Role
from app.models import User
from app.repositories.base_repository import EntityBaseRepository


class UserRepository(EntityBaseRepository[User]):
    def __init__(self, db):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> User | None:
        statement = select(self.model).where(
            self.model.is_deleted.is_(False),
            self.model.email == email,
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_all_employees(self) -> list[User]:
        statement = select(self.model).where(
            self.model.is_deleted.is_(False),
            self.model.role == Role.EMPLOYEE,
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())
