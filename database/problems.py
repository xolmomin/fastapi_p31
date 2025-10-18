from sqlalchemy import UUID, String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import CreatedBaseModel, IDBaseModel


class Problem(IDBaseModel, CreatedBaseModel):
    # class Currency(str, Enum):
    #     EASY = 'easy', 'Easy'
    #     MEDIUM = 'medium', 'Medium'
    #     HARD = 'hard', 'Hard'

    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)  # TODO

    # difficulty: Mapped[str] = mapped_column(SqlEnum(Currency), )
    description: Mapped[str] = mapped_column(String)
    examples: Mapped[list['Example']] = relationship('Example', back_populates='problem')


class Example(IDBaseModel):
    order_number: Mapped[int] = mapped_column(Integer, server_default='1')

    input: Mapped[str] = mapped_column(String)
    output: Mapped[str] = mapped_column(String)
    explanation: Mapped[str] = mapped_column(String)
    problem_id: Mapped[UUID] = mapped_column(ForeignKey('problems.id', ondelete='CASCADE'))
    problem: Mapped[str] = relationship('Problem', back_populates='examples')
