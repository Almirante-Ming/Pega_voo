from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, UTC
from tinto.utils import Booking_Status, Seat_Class, Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    passenger_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    seat_class = Column(SqlEnum(Seat_Class, name="seat_class", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    seat_number = Column(String, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    boarding_time = Column(DateTime(timezone=True), nullable=False)
    arrival_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(SqlEnum(Booking_Status, name="booking_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), default=Booking_Status.MARKED)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Relationships
    flight = relationship("Flight", back_populates="tickets")
    passenger = relationship("Person", back_populates="tickets", foreign_keys=[passenger_id])
    seat = relationship("Seat", back_populates="ticket", uselist=False)
    status_logs = relationship("TicketStatusLog", back_populates="ticket")