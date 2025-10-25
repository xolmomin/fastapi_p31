from enum import Enum

from pydantic import BaseModel, Field


class TopicReadSchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)


class TopicCreateSchema(BaseModel):
    name: str = Field(...)


class ProblemReadSchema(BaseModel):
    class Difficulty(str, Enum):
        EASY = "easy"
        MEDIUM = "medium"
        HARD = "hard"

    id: int = Field(...)
    slug: str = Field(...)
    name: str = Field(...)
    difficulty: Difficulty = Field(Difficulty.EASY)
    description: str = Field(...)


class ProblemCreateSchema(BaseModel):
    class Difficulty(str, Enum):
        EASY = "easy"
        MEDIUM = "medium"
        HARD = "hard"

    name: str = Field(...)
    difficulty: Difficulty = Field(Difficulty.EASY)
    description: str = Field(...)
