from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TopicReadSchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)


class SubmissionReadSchema(BaseModel):
    id: int = Field(...)
    problem_id: int = Field(...)
    status: str = Field(...)
    language_id: str = Field(...)
    runtime: int = Field(...)
    memory: int = Field(...)
    created_at: datetime = Field(...)


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
