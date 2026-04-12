from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ErrorMessages, Role
from app.core.exceptions import ConflictException, NotFoundException
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas import PasswordUpdate, UserCreate, UserRead, UserUpdate
from app.utils.password_helper import hash_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def create_user(self, user_create: UserCreate) -> UserRead:
        email = str(user_create.email)
        existing_user = await self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise ConflictException(ErrorMessages.EMAIL_ALREADY_EXISTS)

        user = User(
            email=email,
            name=user_create.name,
            role=Role.EMPLOYEE,
            password_hash=hash_password(user_create.password),
        )
        self.user_repository.create(user)
        await self.user_repository.commit()

        return UserRead.model_validate(user)

    async def get_all_employees(self) -> list[UserRead]:
        employees = await self.user_repository.get_all_employees()

        return [UserRead.model_validate(employee) for employee in employees]

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> UserRead:
        user = await self.user_repository.get_active_by_id(user_id)

        if user is None:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)

        update_data = user_update.model_dump(exclude_none=True)

        if "email" in update_data:
            existing_user = await self.user_repository.get_by_email(update_data["email"])
            if existing_user is not None and existing_user.id != user.id:
                raise ConflictException(ErrorMessages.EMAIL_ALREADY_EXISTS)
            user.email = update_data["email"]

        if "name" in update_data:
            user.name = update_data["name"]

        await self.user_repository.commit()

        return UserRead.model_validate(user)

    async def deactivate_user(self, user_id: UUID) -> None:
        user = await self.user_repository.get_active_by_id(user_id)

        if user is None:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)

        user.is_deleted = True

        await self.user_repository.commit()

    async def update_password(self, user_id: UUID, password_update: PasswordUpdate) -> None:
        user = await self.user_repository.get_active_by_id(user_id)

        if user is None:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)

        user.password_hash = hash_password(password_update.password)

        await self.user_repository.commit()
