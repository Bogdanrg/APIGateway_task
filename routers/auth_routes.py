from fastapi import APIRouter, Body

from base.classes import AsyncSessionManager
from schemas import SignInModel, SignUpModel, TokenPairModel
from users.services import JWTService, UserService

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])


@auth_router.post("/registration/", response_model=SignUpModel)
async def register_user(user: SignUpModel) -> dict:
    async with AsyncSessionManager() as session:
        await UserService.is_unique_user(session, user)
        user_obj = await UserService.create_user(session, user)
    return user_obj


@auth_router.post("/login/", response_model=TokenPairModel)
async def login_user(user: SignInModel) -> dict:
    async with AsyncSessionManager() as session:
        await UserService.check_credentials(session, user.username, user.password)
        jwt_pair = await JWTService.get_token_pair(user.username)
        return jwt_pair


@auth_router.post("/refresh/", response_model=TokenPairModel)
async def refresh_access_token(refresh_token: str = Body(embed=True)) -> dict:
    async with AsyncSessionManager() as session:
        tokens = await JWTService.refresh_access_token(session, refresh_token)
        return tokens
