from datetime import datetime

from sqlalchemy import DateTime, func, text, BigInteger, delete as sqlalchemy_delete, \
    update as sqlalchemy_update, select, or_, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, selectinload

from core.config import settings


# ----------------------------- ABSTRACTS ----------------------------------
class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception as e:
            print(e)
            await db.rollback()

    @classmethod
    async def create(cls, **kwargs):  # Create
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get(cls, criteria, *, relationship=None):
        query = select(cls).where(criteria)
        if relationship:
            query = query.options(selectinload(relationship))
        return (await db.execute(query)).scalar()

    @classmethod
    async def count(cls):
        query = select(func.count()).select_from(cls)
        return (await db.execute(query)).scalar()

    @classmethod
    async def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def filter(
            cls,
            *criteria,
            relationship=None,
            columns=None,
            use_or=False,
            **filters,
    ):
        """
        #
        # # 1️⃣ Oddiy filter (AND)
        # users = await User.filter(name="Ali", age=25)
        #
        # # 2️⃣ Bitta criterion bilan
        # users = await User.filter(User.email.like('%@gmail.com'))
        #
        # # 3️⃣ Bir nechta criterion OR bilan
        # users = await User.filter(User.age < 18, User.role == "student", use_or=True)
        #
        # # 4️⃣ Faqat ma’lum ustunlarni tanlash
        # names = await User.filter(age=25, columns=[User.name])
        #
        # # 5️⃣ Relationshipni preload qilish
        # users = await User.filter(User.is_active == True, relationship="profile")

        Universal filter for flexible querying.
        Examples:
            await User.filter(name="Ali", age=20)
            await User.filter(User.age > 18, User.name.like('%a%'))
            await User.filter(User.role.in_(['admin', 'editor']), use_or=True)
        """
        if columns:
            query = select(*columns)
        else:
            query = select(cls)

        # Add dynamic filters (**kwargs)
        if filters:
            dynamic_filters = [getattr(cls, k) == v for k, v in filters.items()]
            criteria = (*criteria, *dynamic_filters)

        if criteria:
            query = query.where(or_(*criteria) if use_or else and_(*criteria))

        if relationship:
            query = query.options(selectinload(relationship))

        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def all(cls):
        return (await db.execute(select(cls))).scalars().all()


class Base(DeclarativeBase, AbstractClass):

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


# class SlugBaseModel(Base): # TODO
#     __abstract__ = True
#     slug: Mapped[str] = mapped_column(String(255), unique=True)
#
#     @hybrid_property
#     def slug(self):
#         return re.sub(r'[^a-z0-9]+', '-', self.name.lower())
#
#     @slug.setter
#     def slug(self, value):
#         # You might want to handle setting the slug directly if needed
#         self._slug = value


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
