from enum import Enum

from sqlalchemy import Enum as SqlEnum, Table, Column
from sqlalchemy import ForeignKey, Integer, String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from database.base_model import CreatedBaseModel, IDBaseModel, SlugBaseModel

problem_topics_table = Table(
    "problem_topics_table",
    Base.metadata,
    Column("problem_id", ForeignKey("problems.id"), primary_key=True),
    Column("topic_id", ForeignKey("topics.id"), primary_key=True),
)


class Topic(IDBaseModel):
    name: Mapped[str] = mapped_column(String(255))
    problems: Mapped[list['Problem']] = relationship('Problem', secondary=problem_topics_table, back_populates='topics')


class Problem(IDBaseModel, CreatedBaseModel, SlugBaseModel):
    class Difficulty(str, Enum):
        EASY = 'easy'
        MEDIUM = 'medium'
        HARD = 'hard'

    name: Mapped[str] = mapped_column(String(255))

    difficulty: Mapped['Difficulty'] = mapped_column(SqlEnum(Difficulty, name="difficulty_enum"),
                                                     default=Difficulty.EASY)
    description: Mapped[str] = mapped_column(String)
    examples: Mapped[list['Example']] = relationship('Example', back_populates='problem')
    submissions: Mapped[list['Submission']] = relationship('Submission', back_populates='problem')
    topics: Mapped[list['Topic']] = relationship('Topic', secondary=problem_topics_table, back_populates='problems')


event.listen(Problem.name, 'set', Problem.make_slug, retval=False)


class Language(IDBaseModel):
    name: Mapped[str] = mapped_column(String(255))
    submissions: Mapped[list['Submission']] = relationship('Submission', back_populates='language')


class Submission(IDBaseModel, CreatedBaseModel):
    class Status(str, Enum):
        ACCEPTED = 'accepted'
        WRONG_ANSWER = 'wrong_answer'
        RUNTIME_ERROR = 'runtime_error'
        COMPILE_ERROR = 'compile_error'

    difficulty: Mapped[Status] = mapped_column(SqlEnum(Status, name="status_enum"))
    problem_id: Mapped[int] = mapped_column(ForeignKey('problems.id', ondelete='CASCADE'))
    problem: Mapped['Problem'] = relationship('Problem', back_populates='submissions')

    language_id: Mapped[int] = mapped_column(ForeignKey('languages.id', ondelete='CASCADE'))
    language: Mapped['Language'] = relationship('Language', back_populates='submissions')

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship('User', back_populates='submissions')

    runtime: Mapped[int] = mapped_column(Integer, nullable=True)
    memory: Mapped[int] = mapped_column(Integer, nullable=True)


class Example(IDBaseModel):
    order_number: Mapped[int] = mapped_column(Integer, server_default='1')

    input: Mapped[str] = mapped_column(String)
    output: Mapped[str] = mapped_column(String)
    explanation: Mapped[str] = mapped_column(String)
    problem_id: Mapped[int] = mapped_column(ForeignKey('problems.id', ondelete='CASCADE'))
    problem: Mapped['Problem'] = relationship('Problem', back_populates='examples')
