from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from tinto.utils import Seat_Class, Base


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    seat_number = Column(String, nullable=False)
    seat_class = Column(SqlEnum(Seat_Class, name="seat_class_enum", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)

    __table_args__ = (
        UniqueConstraint('flight_id', 'seat_number', name='unique_flight_seat'),
    )

    flight = relationship("Flight", back_populates="seats")
