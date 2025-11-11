from sqlalchemy import Column, Integer, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, UTC
from tinto.utils import Purchase_Status, Payment_Method, Base


class PurchaseHistory(Base):
    __tablename__ = "purchase_history"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    status = Column(SqlEnum(Purchase_Status, name="purchase_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(SqlEnum(Payment_Method, name="payment_method", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    person = relationship("Person", back_populates="purchase_history")
    tickets = relationship("Ticket", back_populates="purchase")