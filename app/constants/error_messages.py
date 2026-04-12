class ErrorMessages:
    """User-facing strings for validation and API errors."""

    EMAIL_ALREADY_EXISTS = "A user with this email already exists."
    INVALID_OR_EXPIRED_TOKEN = "Invalid or expired token."
    PERMISSION_DENIED = "You do not have permission to perform this action."
    INVALID_NAME_FORMAT = "Name must start with a capital letter for each word and contain only lowercase letters after."
    USER_NOT_FOUND = "User not found."
    INVALID_PASSWORD_FORMAT = "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
    INVALID_END_DATE = "End date must be on or after start date."
