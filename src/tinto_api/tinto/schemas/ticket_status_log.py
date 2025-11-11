from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Any
from tinto.utils import Booking_Status


class TicketStatusLogBase(BaseModel):
    ticket_id: int = Field(..., description="Reference to ticket")
    old_status: Booking_Status = Field(..., description="Previous status")
    new_status: Booking_Status = Field(..., description="New status")
    changed_by: int = Field(..., description="Reference to person who changed status")

    @field_validator('old_status', mode='before')
    @classmethod
    def validate_old_status(cls, v: Any) -> Booking_Status:
        if isinstance(v, str):
            try:
                return Booking_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Booking_Status])}")
        return v

    @field_validator('new_status', mode='before')
    @classmethod
    def validate_new_status(cls, v: Any) -> Booking_Status:
        if isinstance(v, str):
            try:
                return Booking_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Booking_Status])}")
        return v


class TicketStatusLogCreate(TicketStatusLogBase):
    pass


class TicketStatusLog(TicketStatusLogBase):
    id: int
    changed_at: datetime

    model_config = {"from_attributes": True}
