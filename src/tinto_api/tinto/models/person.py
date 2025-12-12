from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, UTC
from tinto.utils import User_Status, User_Type, Gender, Base


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    birth_date = Column(String, nullable=False)
    gender = Column(SqlEnum(Gender, name="gender", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    status = Column(SqlEnum(User_Status, name="user_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), default=User_Status.ACTIVE)
    person_type = Column(SqlEnum(User_Type, name="user_type", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), default=User_Type.CUSTOMER)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    tickets = relationship("Ticket", back_populates="passenger", foreign_keys="Ticket.passenger_id")
    ticket_status_changes = relationship("TicketStatusLog", back_populates="changer")
