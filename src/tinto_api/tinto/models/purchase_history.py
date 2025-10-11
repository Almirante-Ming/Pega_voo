from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, UTC
from tinto.utils import Purchase_Status
from .person import Base


class PurchaseHistory(Base):
    __tablename__ = "purchase_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    status = Column(SqlEnum(Purchase_Status, name="purchase_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    destiny = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    dt_create = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    dt_update = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    # Relationships
    user = relationship("Person", back_populates="purchase_history")
    tickets = relationship("Ticket", back_populates="purchase_history")