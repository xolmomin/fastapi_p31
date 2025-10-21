from pydantic import BaseModel, Field


class TagCreateSchema(BaseModel):
    name: str = Field(...)
    key: str | None = None


class ProblemCreateSchema(BaseModel):
    name: str = Field(...)
    difficulty: str = Field(...)
    description: str = Field(...)
