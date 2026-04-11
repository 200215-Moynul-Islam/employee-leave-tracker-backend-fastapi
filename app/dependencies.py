from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.constants import ErrorMessages
from app.utils.jwt_helper import decode_access_token


bearer_scheme = HTTPBearer()


def validate_token_and_get_payload(
    auth_credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict[str, str]:
    access_token = auth_credentials.credentials

    try:
        token_payload = decode_access_token(access_token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_OR_EXPIRED_TOKEN,
        ) from exc

    return token_payload


def authorize_roles(*allowed_roles: str) -> Callable:
    def role_checker(
        token_payload: dict[str, str] = Depends(validate_token_and_get_payload),
    ) -> None:
        if token_payload.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorMessages.PERMISSION_DENIED,
            )

    return role_checker
