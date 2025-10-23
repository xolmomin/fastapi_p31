from enum import Enum

from pydantic import BaseModel, Field


class TopicCreateSchema(BaseModel):
    name: str = Field(...)
    key: str | None = None


class ProblemCreateSchema(BaseModel):
    class Difficulty(str, Enum):
        EASY = "easy"
        MEDIUM = "medium"
        HARD = "hard"

    name: str = Field(...)
    difficulty: Difficulty = Field(Difficulty.EASY)
    description: str = Field(...)
