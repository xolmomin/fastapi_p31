from pydantic import BaseModel, Field


class TagCreateSchema(BaseModel):
    name: str = Field(...)
    key: str | None = None
