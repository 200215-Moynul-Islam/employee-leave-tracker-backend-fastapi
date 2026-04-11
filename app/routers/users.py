from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import Role
from app.dependencies import authorize_roles
from app.db.dependencies import get_db
from app.schemas import ApiResponse, UserCreate, UserRead
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
        message="User created successfully.",
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
        message="Employees retrieved successfully.",
        data=employees,
    )
