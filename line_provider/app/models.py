from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    coefficient = Column(DECIMAL, nullable=False)
    deadline = Column(DateTime, nullable=False)
    status = Column(String)
