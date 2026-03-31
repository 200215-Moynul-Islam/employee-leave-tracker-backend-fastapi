from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool
    message: str | None = None
    data: Any | None = None
    errors: list[str] | None = None
