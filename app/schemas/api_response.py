from typing import Generic, TypeVar

from pydantic import BaseModel

TData = TypeVar("TData")


class ApiResponse(BaseModel, Generic[TData]):
    success: bool
    message: str | None = None
    data: TData | None = None
    errors: list[str] | None = None
