
from fastapi import Depends
from typing_extensions import Annotated

from app.usecase.requests.user.getting import get_superuser, get_verified_user, get_active_user
from app.usecase.requests.user.shemas import DataUser

SuperUser = Annotated[DataUser, Depends(get_superuser)]
VerifiedUser = Annotated[DataUser, Depends(get_verified_user)]
ActiveUser = Annotated[DataUser, Depends(get_active_user)]
