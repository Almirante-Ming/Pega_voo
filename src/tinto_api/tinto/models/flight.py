from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, UTC
from tinto.utils import Flight_Status, Flight_Class
from .person import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    airline_id = Column(Integer, ForeignKey("airlines.id"), nullable=False)
    flight_number = Column(String, unique=True, nullable=False)
    origin = Column(String, nullable=False)
    destiny = Column(String, nullable=False)
    f_class = Column(SqlEnum(Flight_Class, name="flight_class", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=Flight_Class.ECONOMY)
    departure = Column(DateTime(timezone=True), nullable=False)
    arrival = Column(DateTime(timezone=True), nullable=False)
    a_seats = Column(Integer, nullable=False)
    t_seats = Column(Integer, nullable=False)
    status = Column(SqlEnum(Flight_Status, name="flight_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), default=Flight_Status.SCHEDULED)
    dt_create = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    dt_update = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Relationships
    airline = relationship("Airline", back_populates="flights")
    tickets = relationship("Ticket", back_populates="flight")