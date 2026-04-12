import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.constants import ErrorMessages, ValidationConstants
from app.constants.roles import Role


class UserCreate(BaseModel):
    """Payload for creating a user."""

    email: EmailStr = Field(
        ...,
        max_length=ValidationConstants.User.MAX_EMAIL_LENGTH,
    )
    name: str = Field(
        ...,
        max_length=ValidationConstants.User.MAX_NAME_LENGTH,
    )
    password: str = Field(
        ...,
        min_length=ValidationConstants.User.MIN_PASSWORD_LENGTH,
        max_length=ValidationConstants.User.MAX_PASSWORD_LENGTH,
    )

    @field_validator("email", "name", mode="before")
    @classmethod
    def strip_outer_whitespace(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.fullmatch(ValidationConstants.User.NAME_REGEX, value):
            raise ValueError(ErrorMessages.INVALID_NAME_FORMAT)
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.fullmatch(ValidationConstants.User.PASSWORD_REGEX, value):
            raise ValueError(ErrorMessages.INVALID_PASSWORD_FORMAT)
        return value


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(
        default=None,
        max_length=ValidationConstants.User.MAX_EMAIL_LENGTH,
    )
    name: str | None = Field(
        default=None,
        max_length=ValidationConstants.User.MAX_NAME_LENGTH,
    )

    @field_validator("email", "name", mode="before")
    @classmethod
    def strip_outer_whitespace(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is not None and not re.fullmatch(ValidationConstants.User.NAME_REGEX, value):
            raise ValueError(ErrorMessages.INVALID_NAME_FORMAT)
        return value


class PasswordUpdate(BaseModel):
    password: str = Field(
        ...,
        min_length=ValidationConstants.User.MIN_PASSWORD_LENGTH,
        max_length=ValidationConstants.User.MAX_PASSWORD_LENGTH,
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.fullmatch(ValidationConstants.User.PASSWORD_REGEX, value):
            raise ValueError(ErrorMessages.INVALID_PASSWORD_FORMAT)
        return value


class UserRead(BaseModel):
    """User returned by the API; excludes secrets such as password_hash."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    name: str
    role: str
