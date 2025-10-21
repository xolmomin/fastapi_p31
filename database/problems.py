from enum import Enum

from sqlalchemy import UUID, String, ForeignKey, Integer, Enum as SqlEnum, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import CreatedBaseModel, IDBaseModel, SlugBaseModel


class Tag(IDBaseModel):
    name: Mapped[str] = mapped_column(String(255))


class Problem(IDBaseModel, CreatedBaseModel, SlugBaseModel):
    class Difficulty(str, Enum):
        EASY = 'easy'
        MEDIUM = 'medium'
        HARD = 'hard'

    name: Mapped[str] = mapped_column(String(255))

    difficulty: Mapped[Difficulty] = mapped_column(
        SqlEnum(Difficulty, name="difficulty_enum"), nullable=False, default=Difficulty.EASY
    )
    description: Mapped[str] = mapped_column(String)
    examples: Mapped[list['Example']] = relationship('Example', back_populates='problem')


event.listen(Problem.name, 'set', Problem.make_slug, retval=False)


class Example(IDBaseModel):
    order_number: Mapped[int] = mapped_column(Integer, server_default='1')

    input: Mapped[str] = mapped_column(String)
    output: Mapped[str] = mapped_column(String)
    explanation: Mapped[str] = mapped_column(String)
    problem_id: Mapped[UUID] = mapped_column(ForeignKey('problems.id', ondelete='CASCADE'))
    problem: Mapped[str] = relationship('Problem', back_populates='examples')
