class BusinessException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidCredentialsException(BusinessException):
    def __init__(self, message: str = "Invalid email or password."):
        super().__init__(message)


class ConflictException(BusinessException):
    def __init__(self, message: str = "Conflict occurred."):
        super().__init__(message)


class NotFoundException(BusinessException):
    def __init__(self, message: str = "Resource not found."):
        super().__init__(message)
