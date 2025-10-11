from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, UTC
from tinto.utils import Booking_Status
from .person import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    purchase_history_id = Column(Integer, ForeignKey("purchase_history.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    passengers = Column(Text, nullable=False)  # JSON string with passenger information
    valor = Column(DECIMAL(10, 2), nullable=False)  # ticket price
    horario_embarque = Column(DateTime(timezone=True), nullable=False)  # boarding time
    horario_desembarque = Column(DateTime(timezone=True), nullable=False)  # arrival time
    status = Column(SqlEnum(Booking_Status, name="booking_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), default=Booking_Status.MARKED)
    dt_create = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    dt_update = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Relationships
    purchase_history = relationship("PurchaseHistory", back_populates="tickets")
    flight = relationship("Flight", back_populates="tickets")
    ticket_passengers = relationship("TicketPassenger", back_populates="ticket")