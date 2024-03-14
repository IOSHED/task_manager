from typing import Union

import requests
from fastapi import Request

from app.main import settings
from app.usecase.requests.user.shemas import DataUser
from app.domain.shemas.response.error import Http401Error


def __get_current_user(request: Request) -> Union[DataUser, Http401Error]:
    """Отправляет запрос на `auth_service` и получает данные о текущем пользователе."""
    jwt_token = request.cookies.get("bonds")
    response = requests.get(settings.request.get_current_user, cookies={'bonds': jwt_token})
    user_info = response.json()
    if 'detail' in user_info:
        return Http401Error(detail="Unauthorized")
    return DataUser(**user_info)


def get_active_user(request: Request) -> Union[DataUser, Http401Error]:
    """Возвращает текущего пользователя, если он активен."""
    current_user = __get_current_user(request)
    if isinstance(current_user, Http401Error):
        return current_user
    if current_user.is_active:
        return current_user
    return Http401Error(detail="Current user is not active")


def get_verified_user(request: Request) -> Union[DataUser, Http401Error]:
    """Возвращает текущего пользователя, если он верифицирован."""
    current_user = __get_current_user(request)
    if isinstance(current_user, Http401Error):
        return current_user
    if current_user.is_active and current_user.is_verified:
        return current_user
    return Http401Error(detail="Email not verified")


def get_superuser(request: Request) -> Union[DataUser, Http401Error]:
    """Возвращает текущего пользователя, если он админ."""
    current_user = __get_current_user(request)
    if isinstance(current_user, Http401Error):
        return current_user
    if current_user.is_superuser:
        return current_user
    return Http401Error(detail="Current user is not admin")
