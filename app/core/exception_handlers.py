from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.constants import ResponseMessages
from app.core.exceptions import (
    BusinessException,
    ConflictException,
    InvalidCredentialsException,
    NotFoundException,
)
from app.schemas import ApiResponse


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        response = ApiResponse(
            success=False,
            message=ResponseMessages.VALIDATION_FAILED,
            errors=[
                error.get("msg", ResponseMessages.INVALID_REQUEST)
                for error in exc.errors()
            ],
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=response.model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        errors = exc.detail if isinstance(exc.detail, list) else [str(exc.detail)]
        response = ApiResponse(
            success=False,
            message=ResponseMessages.REQUEST_FAILED,
            errors=errors,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(),
        )

    @app.exception_handler(BusinessException)
    async def business_exception_handler(
        request: Request,
        exc: BusinessException,
    ) -> JSONResponse:
        response = ApiResponse(
            success=False,
            message=ResponseMessages.REQUEST_FAILED,
            errors=[exc.message],
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.model_dump(),
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_exception_handler(
        request: Request,
        exc: InvalidCredentialsException,
    ) -> JSONResponse:
        response = ApiResponse(
            success=False,
            message=ResponseMessages.LOGIN_FAILED,
            errors=[exc.message],
        )

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=response.model_dump(),
        )

    @app.exception_handler(ConflictException)
    async def conflict_exception_handler(
        request: Request,
        exc: ConflictException,
    ) -> JSONResponse:
        response = ApiResponse(
            success=False,
            message=ResponseMessages.REQUEST_FAILED,
            errors=[exc.message],
        )

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response.model_dump(),
        )

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(
        request: Request,
        exc: NotFoundException,
    ) -> JSONResponse:
        response = ApiResponse(
            success=False,
            message=ResponseMessages.REQUEST_FAILED,
            errors=[exc.message],
        )

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response.model_dump(),
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        response = ApiResponse(
            success=False,
            message=ResponseMessages.INTERNAL_SERVER_ERROR,
            errors=[ResponseMessages.UNEXPECTED_ERROR_OCCURRED],
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump(),
        )
