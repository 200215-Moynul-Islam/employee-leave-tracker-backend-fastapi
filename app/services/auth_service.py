from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidCredentialsException
from app.repositories.user_repository import UserRepository
from app.schemas import AuthTokenData, LoginInput
from app.utils.jwt_helper import create_access_token
from app.utils.password_helper import verify_password


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def authenticate_user(self, login_input: LoginInput, expires_in_minutes: int) -> AuthTokenData:
        user = await self.user_repository.get_by_email(str(login_input.email))

        if user is None:
            raise InvalidCredentialsException()

        if not verify_password(login_input.password, user.password_hash):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            subject=str(user.id),
            additional_claims={
                "email": user.email,
                "role": user.role,
            },
        )

        return AuthTokenData(
            access_token=access_token,
            expires_in_seconds=expires_in_minutes * 60,
        )
