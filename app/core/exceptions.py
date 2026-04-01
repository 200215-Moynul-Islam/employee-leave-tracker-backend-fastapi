class BusinessException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidCredentialsError(BusinessException):
    def __init__(self, message: str = "Invalid email or password."):
        super().__init__(message)
