from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base_model import CreatedBaseModel, IDBaseModel


class User(IDBaseModel, CreatedBaseModel):
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))

    # @classmethod
    # async def create(cls, **kwargs):
    #     from utils.security import get_password_hash
    #     kwargs['password'] = get_password_hash(kwargs.get('password'))
    #     return await super().create(**kwargs)
