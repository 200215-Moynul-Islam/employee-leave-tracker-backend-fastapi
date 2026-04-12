from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

from app.constants import ErrorMessages, LeaveRequestStatus


class LeaveRequestCreate(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self) -> "LeaveRequestCreate":
        if self.end_date < self.start_date:
            raise ValueError(ErrorMessages.INVALID_END_DATE_FORMAT)

        return self


class LeaveRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    start_date: date
    end_date: date
    created_at: date
    status: LeaveRequestStatus
    user_id: UUID
