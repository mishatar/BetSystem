from sqlalchemy import (CheckConstraint, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import declarative_base, relationship
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

    bets = relationship("Bet", back_populates="event")

    __table_args__ = (
        CheckConstraint(
            "status IN (1, 2, 3)",
            name="check_status_valid_values"
        ),
    )


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    status = Column(String)
    timestamp = Column(DateTime, nullable=False)

    event = relationship("Event", back_populates="bets")
