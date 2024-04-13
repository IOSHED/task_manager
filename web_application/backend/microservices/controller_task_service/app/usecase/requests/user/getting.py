from typing import Union

import requests
from fastapi import Request

from app.usecase.requests.user.shemas import DataUser
from app.usecase.error.handler import Http401Error
from app.infra.config.config import Settings


SETTINGS = Settings()


def __get_current_user(request: Request) -> Union[DataUser, Http401Error]:
    """Send request to `auth_service` and git data about current user"""
    jwt_token = request.cookies.get("bonds")
    response = requests.get(SETTINGS.request.get_current_user, cookies={'bonds': jwt_token})
    user_info = response.json()
    if 'detail' in user_info:
        raise Http401Error(detail="Unauthorized")
    return DataUser(**user_info)


def get_active_user(request: Request) -> Union[DataUser, Http401Error]:
    """Return current user if he is active."""
    current_user = __get_current_user(request)
    if isinstance(current_user, Http401Error):
        return current_user
    if current_user.is_active:
        return current_user
    return Http401Error(detail="Current user is not active")


def get_verified_user(request: Request) -> Union[DataUser, Http401Error]:
    """Return current user if he is verified."""
    current_user = __get_current_user(request)
    if isinstance(current_user, Http401Error):
        return current_user
    if current_user.is_active and current_user.is_verified:
        return current_user
    raise Http401Error(detail="Email not verified")


def get_superuser(request: Request) -> Union[DataUser, Http401Error]:
    """Return current user if he is admin."""
    current_user = __get_current_user(request)
    if isinstance(current_user, Http401Error):
        return current_user
    if current_user.is_superuser:
        return current_user
    raise Http401Error(detail="Current user is not admin")
