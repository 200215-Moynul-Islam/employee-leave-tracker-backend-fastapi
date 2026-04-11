from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ErrorMessages, Role
from app.core.exceptions import ConflictException
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserRead
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
        user = await self.user_repository.create(user)

        return UserRead.model_validate(user)
