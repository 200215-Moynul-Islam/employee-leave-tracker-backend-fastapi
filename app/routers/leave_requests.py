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
