
from pydantic import BaseModel


class HTTPError(BaseModel):
    """
    HTTP error schema to be used when an `HTTPException` is thrown.
    """

    detail: str
