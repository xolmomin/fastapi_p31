from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    message: str = "Success"
    data: T | None = None
