from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, UTC
from tinto.utils import Flight_Status, Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    airline_id = Column(Integer, ForeignKey("airlines.id"), nullable=False)
    aircraft_model = Column(String, nullable=False)
    flight_number = Column(String, unique=True, nullable=False)
    origin_city = Column(String, nullable=False)
    origin_airport = Column(String, nullable=False)
    destination_city = Column(String, nullable=False)
    destination_airport = Column(String, nullable=False)
    departure_time = Column(DateTime(timezone=True), nullable=False)
    estimated_arrival = Column(DateTime(timezone=True), nullable=False)
    stops_count = Column(Integer, nullable=False, default=0)
    avaliable_seats = Column(Integer, nullable=False)
    economy_seats = Column(Integer, nullable=False)
    premium_seats = Column(Integer, nullable=False)
    status = Column(SqlEnum(Flight_Status, name="flight_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), default=Flight_Status.SCHEDULED)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    airline = relationship("Airline", back_populates="flights")
    tickets = relationship("Ticket", back_populates="flight")
    seats = relationship("Seat", back_populates="flight")