from typing import List

import pydantic
from sqlalchemy import insert, update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.usecase.repository import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = NotImplementedError
    view_schema: pydantic.BaseModel = NotImplementedError

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, data: dict, **filter_by) -> int:
        stmt = update(self.model).values(**data).filter_by(**filter_by).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self) -> List[pydantic.BaseModel]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [self.view_schema.model_validate(row, from_attributes=True) for row in res.all()]
        return res

    async def find_one(self, **filter_by) -> pydantic.BaseModel:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = self.view_schema.model_validate(res.scalar_one(), from_attributes=True)
        return res

    async def delete_all(self):
        stmt = delete(self.model)
        await self.session.execute(stmt)

    async def delete_one(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
