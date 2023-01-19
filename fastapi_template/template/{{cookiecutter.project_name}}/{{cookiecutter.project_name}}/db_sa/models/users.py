import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, schemas
from fastapi_users.authentication import (AuthenticationBackend, BearerTransport,
                                          CookieTransport, JWTStrategy)
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from sqlalchemy.ext.asyncio import AsyncSession
from {{cookiecutter.project_name}}.db.base import Base
from {{cookiecutter.project_name}}.db.dependencies import get_db_session
from {{cookiecutter.project_name}}.settings import settings


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.users_secret
    verification_token_secret = settings.users_secret


async def get_user_db(session: AsyncSession = Depends(get_db_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

    
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.users_secret, lifetime_seconds=3600)


{%- if cookiecutter.jwt_auth == "True" %}
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
auth_jwt = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
{%- endif %}

{%- if cookiecutter.cookie_auth == "True" %}
cookie_transport = CookieTransport(cookie_max_age=3600)
auth_cookie = AuthenticationBackend(
    name="cookie", transport=cookie_transport, get_strategy=get_jwt_strategy
)
{%- endif %}

backends = [
    {%- if cookiecutter.cookie_auth == "True" %}auth_cookie,{%- endif %}
    {%- if cookiecutter.jwt_auth == "True" %}auth_jwt,{%- endif %}
]

api_users = FastAPIUsers[User, uuid.UUID](get_user_manager, backends)

current_active_user = api_users.current_user(active=True)
