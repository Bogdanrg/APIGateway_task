from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from base.classes import AsyncSessionManager
from exceptions import AuthenticationSchemeException, AuthorizationCodeException
from repos.user_repo import UserRepository
from users.services import JWTService


class JWTBearer(HTTPBearer):
    def __init__(self) -> None:
        super(JWTBearer, self).__init__(auto_error=False)

    async def __call__(self, request: Request) -> None:
        async with AsyncSessionManager() as session:
            credentials: HTTPAuthorizationCredentials = await super(
                JWTBearer, self
            ).__call__(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise AuthenticationSchemeException(
                        status_code=403, detail="Invalid authentication scheme."
                    )
                payload: dict = await JWTService.decode_token(credentials.credentials)
                request.state.user = await UserRepository.get_user_by_username(
                    payload["username"], session
                )
            else:
                raise AuthorizationCodeException(
                    status_code=403, detail="Invalid authorization code."
                )
