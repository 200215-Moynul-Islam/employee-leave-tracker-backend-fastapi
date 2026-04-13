from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ErrorMessages, LeaveRequestStatus, Role
from app.core.exceptions import BusinessException, NotFoundException
from app.models import LeaveRequest
from app.repositories.leave_request_repository import LeaveRequestRepository
from app.repositories.user_repository import UserRepository
from app.schemas import LeaveRequestCreate, LeaveRequestRead, LeaveRequestWithUserRead


class LeaveRequestService:
    def __init__(self, db: AsyncSession):
        self.leave_request_repository = LeaveRequestRepository(db)
        self.user_repository = UserRepository(db)

    async def create_leave_request(
        self,
        user_id: UUID,
        leave_request_create: LeaveRequestCreate,
    ) -> LeaveRequestRead:
        user = await self.user_repository.get_active_by_id(user_id)

        if user is None:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)

        leave_request = LeaveRequest(
            start_date=leave_request_create.start_date,
            end_date=leave_request_create.end_date,
            created_at=date.today(),
            status=LeaveRequestStatus.PENDING,
            user_id=user_id,
        )
        self.leave_request_repository.create(leave_request)
        await self.leave_request_repository.commit()

        return LeaveRequestRead.model_validate(leave_request)

    async def get_all_leave_requests(self) -> list[LeaveRequestWithUserRead]:
        leave_requests = await self.leave_request_repository.get_all_active_with_users()

        return [LeaveRequestWithUserRead.model_validate(leave_request) for leave_request in leave_requests]

    async def delete_leave_request(
        self,
        user_id: UUID,
        leave_request_id: UUID,
    ) -> None:
        user = await self.user_repository.get_active_by_id(user_id)

        if user is None:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)

        leave_request = await self.leave_request_repository.get_active_by_id(leave_request_id)

        if leave_request is None or leave_request.user_id != user_id:
            raise NotFoundException(ErrorMessages.LEAVE_REQUEST_NOT_FOUND)

        if leave_request.status != LeaveRequestStatus.PENDING:
            raise BusinessException(
                ErrorMessages.LEAVE_REQUEST_NOT_PENDING
            )

        leave_request.is_deleted = True

        await self.leave_request_repository.commit()

    async def approve_leave_request(
        self,
        leave_request_id: UUID,
    ) -> LeaveRequestRead:
        leave_request = await self.leave_request_repository.get_active_by_id(leave_request_id)

        if leave_request is None:
            raise NotFoundException(ErrorMessages.LEAVE_REQUEST_NOT_FOUND)

        if leave_request.status != LeaveRequestStatus.PENDING:
            raise BusinessException(
                ErrorMessages.LEAVE_REQUEST_NOT_PENDING
            )

        leave_request.status = LeaveRequestStatus.APPROVED
        await self.leave_request_repository.commit()

        return LeaveRequestRead.model_validate(leave_request)

    async def reject_leave_request(
        self,
        leave_request_id: UUID,
    ) -> LeaveRequestRead:
        leave_request = await self.leave_request_repository.get_active_by_id(leave_request_id)

        if leave_request is None:
            raise NotFoundException(ErrorMessages.LEAVE_REQUEST_NOT_FOUND)

        if leave_request.status != LeaveRequestStatus.PENDING:
            raise BusinessException(
                ErrorMessages.LEAVE_REQUEST_NOT_PENDING
            )

        leave_request.status = LeaveRequestStatus.REJECTED
        await self.leave_request_repository.commit()

        return LeaveRequestRead.model_validate(leave_request)
