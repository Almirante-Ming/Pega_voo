from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from tinto.utils import Base


class TicketPassenger(Base):
    __tablename__ = "ticket_passengers"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)

    ticket = relationship("Ticket", back_populates="ticket_passengers")
    person = relationship("Person", back_populates="passenger_tickets")