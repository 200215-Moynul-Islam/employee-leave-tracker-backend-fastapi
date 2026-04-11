from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.dependencies import get_db
from app.schemas import ApiResponse, AuthTokenData, LoginInput
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=ApiResponse[AuthTokenData], status_code=status.HTTP_200_OK)
async def login(
    login_input: LoginInput,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[AuthTokenData]:
    auth_service = AuthService(db)
    auth_token = await auth_service.authenticate_user(
        login_input=login_input,
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    return ApiResponse[AuthTokenData](
        success=True,
        message="Login successful.",
        data=auth_token,
    )
