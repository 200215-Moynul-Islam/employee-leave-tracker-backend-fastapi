from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ResponseMessages, Role
from app.dependencies import authorize_roles, validate_token_and_get_payload
from app.db.dependencies import get_db
from app.schemas import ApiResponse, PasswordUpdate, UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=ApiResponse[UserRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(authorize_roles(Role.ADMIN))],
)
async def create_user(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[UserRead]:
    user_service = UserService(db)
    user = await user_service.create_user(user_create)

    return ApiResponse[UserRead](
        success=True,
        message=ResponseMessages.USER_CREATION_SUCCESS,
        data=user,
    )


@router.get(
    "/employees",
    response_model=ApiResponse[list[UserRead]],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(authorize_roles(Role.ADMIN))],
)
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[list[UserRead]]:
    user_service = UserService(db)
    employees = await user_service.get_all_employees()

    return ApiResponse[list[UserRead]](
        success=True,
        message=ResponseMessages.EMPLOYEES_RETRIEVAL_SUCCESS,
        data=employees,
    )


@router.patch(
    "/{user_id}",
    response_model=ApiResponse[UserRead],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(authorize_roles(Role.ADMIN))],
)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[UserRead]:
    user_service = UserService(db)
    user = await user_service.update_user(user_id, user_update)

    return ApiResponse[UserRead](
        success=True,
        message=ResponseMessages.USER_UPDATE_SUCCESS,
        data=user,
    )


@router.delete(
    "/{user_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(authorize_roles(Role.ADMIN))],
)
async def deactivate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[None]:
    user_service = UserService(db)
    await user_service.deactivate_user(user_id)

    return ApiResponse[None](
        success=True,
        message=ResponseMessages.USER_DELETION_SUCCESS,
    )


@router.patch(
    "/me/password",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
)
async def update_user_password(
    password_update: PasswordUpdate,
    db: AsyncSession = Depends(get_db),
    token_payload: dict[str, str] = Depends(validate_token_and_get_payload),
) -> ApiResponse[None]:
    user_service = UserService(db)
    current_user_id = UUID(token_payload["sub"])
    await user_service.update_password(current_user_id, password_update)

    return ApiResponse[None](
        success=True,
        message=ResponseMessages.PASSWORD_UPDATE_SUCCESS,
    )
