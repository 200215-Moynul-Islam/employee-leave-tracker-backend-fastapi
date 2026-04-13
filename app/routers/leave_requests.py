from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ResponseMessages, Role
from app.db.dependencies import get_db
from app.dependencies import authorize_roles, validate_token_and_get_payload
from app.schemas import ApiResponse, LeaveRequestCreate, LeaveRequestRead
from app.services.leave_request_service import LeaveRequestService


router = APIRouter(prefix="/leave-requests", tags=["Leave Requests"])


@router.post(
    "/me",
    response_model=ApiResponse[LeaveRequestRead],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(authorize_roles(Role.EMPLOYEE))],
)
async def create_leave_request(
    leave_request_create: LeaveRequestCreate,
    db: AsyncSession = Depends(get_db),
    token_payload: dict[str, str] = Depends(validate_token_and_get_payload),
) -> ApiResponse[LeaveRequestRead]:
    leave_request_service = LeaveRequestService(db)
    current_user_id = UUID(token_payload["sub"])
    leave_request = await leave_request_service.create_leave_request(
        user_id=current_user_id,
        leave_request_create=leave_request_create,
    )

    return ApiResponse[LeaveRequestRead](
        success=True,
        message=ResponseMessages.LEAVE_REQUEST_CREATION_SUCCESS,
        data=leave_request,
    )


@router.delete(
    "/me/{leave_request_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(authorize_roles(Role.EMPLOYEE))],
)
async def delete_leave_request(
    leave_request_id: UUID,
    db: AsyncSession = Depends(get_db),
    token_payload: dict[str, str] = Depends(validate_token_and_get_payload),
) -> ApiResponse[None]:
    leave_request_service = LeaveRequestService(db)
    current_user_id = UUID(token_payload["sub"])
    await leave_request_service.delete_leave_request(
        user_id=current_user_id,
        leave_request_id=leave_request_id,
    )

    return ApiResponse[None](
        success=True,
        message=ResponseMessages.LEAVE_REQUEST_DELETION_SUCCESS,
    )


@router.patch(
    "/{leave_request_id}/approve",
    response_model=ApiResponse[LeaveRequestRead],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(authorize_roles(Role.ADMIN))],
)
async def approve_leave_request(
    leave_request_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[LeaveRequestRead]:
    leave_request_service = LeaveRequestService(db)
    leave_request = await leave_request_service.approve_leave_request(
        leave_request_id=leave_request_id,
    )

    return ApiResponse[LeaveRequestRead](
        success=True,
        message=ResponseMessages.LEAVE_REQUEST_APPROVAL_SUCCESS,
        data=leave_request,
    )
