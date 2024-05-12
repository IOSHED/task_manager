from typing import Union

from fastapi import Depends
from typing_extensions import Annotated

from app.usecase.requests.user.getting import get_superuser, get_verified_user, get_active_user
from app.usecase.requests.user.shemas import DataUser
from app.usecase.error.handler import Http401Error

SuperUser = Annotated[Union[DataUser, Http401Error], Depends(get_superuser)]
VerifiedUser = Annotated[Union[DataUser, Http401Error], Depends(get_verified_user)]
ActiveUser = Annotated[Union[DataUser, Http401Error], Depends(get_active_user)]
