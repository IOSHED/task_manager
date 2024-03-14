from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.infra.config.enums import Mode
from app.infra.config.config import Settings

SETTINGS = Settings()


class Base(DeclarativeBase):
    pass


engine = create_async_engine(SETTINGS.database.postgres.database_url, echo=False)
if SETTINGS.mode == Mode.local:
    engine.echo = True

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
