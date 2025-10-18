from datetime import datetime

from sqlalchemy import DateTime, func, text, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from core.config import settings


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(self) -> str:
        name = self.__name__.lower()
        return name + 's'


class UUIDBaseModel(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))


class IDBaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)


class CreatedBaseModel(Base):
    __abstract__ = True

    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Database:

    def __init__(self):
        self._engine = None
        self._session = None

    def __getattr__(self, item):
        return getattr(self._session, item)

    def init(self):
        self._engine = create_async_engine(settings.async_postgresql_url)
        self._session = async_sessionmaker(self._engine, expire_on_commit=False)()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db = Database()
db.init()
