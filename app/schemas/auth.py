import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.constants import ErrorMessages, ValidationConstants


class LoginInput(BaseModel):
    email: EmailStr = Field(
        ...,
        max_length=ValidationConstants.User.MAX_EMAIL_LENGTH
    )
    password: str = Field(
        ...,
        min_length=ValidationConstants.User.MIN_PASSWORD_LENGTH,
        max_length=ValidationConstants.User.MAX_PASSWORD_LENGTH,
    )

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.fullmatch(ValidationConstants.User.PASSWORD_REGEX, value):
            raise ValueError(ErrorMessages.INVALID_PASSWORD_FORMAT)
        return value


class AuthTokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
