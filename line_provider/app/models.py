from sqlalchemy import CheckConstraint, Column, DateTime, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import DECIMAL

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    coefficient = Column(DECIMAL, nullable=False)
    deadline = Column(DateTime, nullable=False)
    status = Column(
        Integer,
        nullable=False,
        comment="1 - NEW, 2 - FINISHED_WIN, 3 - FINISHED_LOSE"
    )
    __table_args__ = (
        CheckConstraint(
            "status IN (1, 2, 3)",
            name="check_status_valid_values"
        ),
    )
