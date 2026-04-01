from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidCredentialsError
from app.repositories.user_repository import UserRepository
from app.schemas import AuthTokenData, LoginInput
from app.utils.jwt_helper import create_access_token
from app.utils.password_helper import verify_password


class AuthService:
    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        login_input: LoginInput,
        expires_in_minutes: int,
    ) -> AuthTokenData:
        user = await UserRepository.get_by_email(db, str(login_input.email))

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(login_input.password, user.password_hash):
            raise InvalidCredentialsError()

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
