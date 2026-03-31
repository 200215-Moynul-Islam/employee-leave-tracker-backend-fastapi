from pydantic import BaseModel, EmailStr, Field, field_validator

from app.constants import ValidationConstants


class LoginInput(BaseModel):
    email: EmailStr = Field(
        ...,
        min_length=ValidationConstants.User.MIN_EMAIL_LENGTH,
        max_length=ValidationConstants.User.MAX_EMAIL_LENGTH
    )
    password: str = Field(
        ...,
        min_length=ValidationConstants.User.MIN_PASSWORD_LENGTH,
        max_length=ValidationConstants.User.MAX_PASSWORD_LENGTH,
        pattern=ValidationConstants.User.PASSWORD_REGEX,
    )

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value
