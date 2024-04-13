from typing import Dict, Any

from fastapi import HTTPException
from starlette import status


class HttpError(HTTPException):
    status_code: int = NotImplementedError

    def __init__(self, detail: Dict[str, Any] | str) -> None:
        super(HTTPException, self).__init__(status_code=self.status_code, detail=detail)


class Http401Error(HttpError):
    status_code: int = status.HTTP_401_UNAUTHORIZED

    def __init__(self, detail: Dict[str, Any] | str = "") -> None:
        super(HTTPException, self).__init__(status_code=self.status_code, detail=detail)


class Http404Error(HttpError):
    status_code: int = status.HTTP_404_NOT_FOUND

    def __init__(self, detail: Dict[str, Any] | str) -> None:
        super(HTTPException, self).__init__(status_code=self.status_code, detail=detail)


class Http500Error(HttpError):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: Dict[str, Any] | str) -> None:
        super(HTTPException, self).__init__(status_code=self.status_code, detail=detail)
