import datetime

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config import app_settings
from repos.user_repo import UserRepository
from schemas import SignUpModel
from users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HasherService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)


class UserService:
    @staticmethod
    async def is_unique_user(session: AsyncSession, user: SignUpModel) -> None:
        user_username = await UserRepository.get_user_by_username(
            user.username, session
        )
        if user_username is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username must be unique",
            )
        user_email = await UserRepository.get_user_by_email(user.email, session)
        if user_email is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email must be unique"
            )

    @staticmethod
    async def create_user(session: AsyncSession, user: SignUpModel) -> Result[User]:
        user = await UserRepository.insert_one(
            session,
            username=user.username,
            email=user.email,
            password=HasherService.get_password_hash(user.password),
        )
        return user

    @staticmethod
    async def check_credentials(
        session: AsyncSession, username: str, password: str
    ) -> None:
        user = await UserRepository.get_user_by_username(username, session)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid user")
        if not HasherService.verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Invalid password")


class JWTService:
    @staticmethod
    async def get_token_pair(username: str) -> dict:
        access_token = await JWTService.encode_access_token(username)
        refresh_token = await JWTService.encode_refresh_token(username)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    @staticmethod
    async def encode_access_token(username: str) -> str:
        access_token = jwt.encode(
            {
                "username": username,
                "type": "access_token",
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(minutes=5),
            },
            app_settings.SECRET,
            algorithm=app_settings.ALGORITHM,
        )
        return access_token

    @staticmethod
    async def encode_refresh_token(username: str) -> str:
        refresh_token = jwt.encode(
            {
                "username": username,
                "type": "refresh_token",
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(hours=24),
            },
            app_settings.SECRET,
            algorithm=app_settings.ALGORITHM,
        )
        return refresh_token

    @staticmethod
    async def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                app_settings.SECRET,
                algorithms=app_settings.ALGORITHM,
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Token has been expired"
            )
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )

    @staticmethod
    async def refresh_access_token(session: AsyncSession, refresh_token: str) -> dict:
        payload: dict = await JWTService.decode_token(refresh_token)
        if payload:
            token_type = payload.get("type", "")
            if token_type != "refresh_token":
                raise HTTPException(status_code=400, detail="Wrong token type")
            user = await UserRepository.get_user_by_username(
                payload.get("username", ""), session
            )
            if user:
                access_token = await JWTService.encode_access_token(
                    payload.get("username", "")
                )
                tokens = {"access_token": access_token, "refresh_token": refresh_token}
                return tokens

        raise HTTPException(status_code=400, detail="Invalid refresh token")
