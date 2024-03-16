from typing import AsyncGenerator, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.infra.config.enums import Mode
from app.infra.config.config import Settings


SETTINGS = Settings()


class Base(DeclarativeBase):
    _repr_field: List[str] | Tuple[str] = []

    def __repr__(self) -> str:
        """Return string: <ClassName repr_field = value_repr_field>. Where the repr_field is cls field you class."""
        columns = []
        for col in self.__table__.columns.keys():
            if col in self._repr_field:
                columns.append(f"{col} = {getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(columns)}>"


engine = create_async_engine(SETTINGS.database.postgres.database_url, echo=True)
if SETTINGS.mode == Mode.dev:
    engine.echo = False

async_session_maker = async_sessionmaker(engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
