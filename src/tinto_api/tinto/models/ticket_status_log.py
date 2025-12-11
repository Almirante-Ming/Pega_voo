from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, UTC
from tinto.utils import Booking_Status, Base


class TicketStatusLog(Base):
    __tablename__ = "ticket_status_log"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    old_status = Column(SqlEnum(Booking_Status, name="old_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    new_status = Column(SqlEnum(Booking_Status, name="new_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    changed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    changed_by = Column(Integer, ForeignKey("persons.id"), nullable=False)

    changer = relationship("Person", back_populates="ticket_status_changes")
