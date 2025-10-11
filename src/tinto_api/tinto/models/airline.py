from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, UTC
from tinto.utils import User_Status
from .person import Base


class Airline(Base):
    __tablename__ = "airlines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    status = Column(SqlEnum(User_Status, name="airline_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), default=User_Status.ACTIVE)
    dt_create = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    dt_update = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Relationships
    flights = relationship("Flight", back_populates="airline")