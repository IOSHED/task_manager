from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.infra.config.enums import Mode
from app.main import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.database.postgres.database_url, echo=False)
if settings.mode == Mode.local:
    engine.echo = True

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
