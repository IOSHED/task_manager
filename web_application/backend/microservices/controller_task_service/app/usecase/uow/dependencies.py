from typing_extensions import Annotated

from fastapi import Depends

from app.usecase.uow.interface import IUnitOfWork
from app.usecase.uow.unitofwork import UnitOfWork


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
