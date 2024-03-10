from abc import ABC
from typing import Dict, Any

import pydantic
from pydantic import PositiveInt, field_validator
from starlette import status


class HttpError(pydantic.BaseModel, ABC):
    statuscode: PositiveInt = NotImplementedError
    detail: Dict[str, Any] | str = NotImplementedError

    @classmethod
    @field_validator("statuscode")
    def validate_statuscode_for_error(cls, v: PositiveInt) -> PositiveInt:
        if 400 <= v <= 500:
            return v
        raise ValueError('status code error will should in range to 400 from 500')


class Http401Error(HttpError):
    statuscode: PositiveInt = status.HTTP_401_UNAUTHORIZED
    detail: Dict[str, Any] | str = NotImplementedError


class Http404Error(HttpError):
    statuscode: PositiveInt = status.HTTP_404_NOT_FOUND
    detail: Dict[str, Any] | str = NotImplementedError


class Http500Error(HttpError):
    statuscode: PositiveInt = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: Dict[str, Any] | str = NotImplementedError
