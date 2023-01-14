from fastapi import APIRouter

from {{cookiecutter.project_name}}.db.models.users import (UserCreate,
                                                           UserRead,
                                                           UserUpdate,
                                                           api_users,
                                                           auth_backend,
                                                           auth_cookie)


router = APIRouter()

router.include_router(
    api_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    api_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    api_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    api_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

router.include_router(
    api_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

router.include_router(
    api_users.get_auth_router(auth_cookie),
    prefix="/auth/cookie",
    tags=["auth"]
)
