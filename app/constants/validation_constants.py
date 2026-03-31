class ValidationConstants:
    class User:
        MAX_NAME_LENGTH = 100
        NAME_REGEX = r"^[A-Z][a-z]*(?: [A-Z][a-z]*)*$"
        MAX_EMAIL_LENGTH = 254
        MAX_ROLE_LENGTH = 50
        MIN_PASSWORD_LENGTH = 8
        MAX_PASSWORD_LENGTH = 64
        PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).+$"

    class Leave:
        MAX_STATUS_LENGTH = 50
