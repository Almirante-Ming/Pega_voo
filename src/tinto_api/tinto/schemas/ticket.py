from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Any
from decimal import Decimal
from tinto.utils import Seat_Class


class TicketBase(BaseModel):
    flight_id: int = Field(..., description="Reference to flight")
    passenger_id: int = Field(..., description="Reference to passenger (person)")
    seat_class: Seat_Class = Field(..., description="Seat class")
    price: Decimal = Field(..., description="Ticket price")
    boarding_time: datetime = Field(..., description="Boarding time for the flight")
    arrival_time: datetime = Field(..., description="Arrival time for the flight")
    status: str = Field(default="disponível", description="Ticket status")

    @field_validator('seat_class', mode='before')
    @classmethod
    def validate_seat_class(cls, v: Any) -> Seat_Class:
        if isinstance(v, str):
            try:
                return Seat_Class(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Seat_Class])}")
        return v


class TicketCreate(BaseModel):
    flight_id: int = Field(..., description="Reference to flight")
    seat_number: str = Field(..., description="Seat number")


class TicketUpdate(BaseModel):
    flight_id: Optional[int] = None
    passenger_id: Optional[int] = None
    seat_class: Optional[Seat_Class] = None
    price: Optional[Decimal] = None
    boarding_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    status: Optional[str] = None

    @field_validator('seat_class', mode='before')
    @classmethod
    def validate_seat_class_update(cls, v: Any) -> Optional[Seat_Class]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return Seat_Class(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Seat_Class])}")
        return v


class Ticket(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TicketCheckoutResponse(BaseModel):
    """Response returned after successful ticket reservation and checkout session creation"""
    ticket_id: int = Field(..., description="ID of the reserved ticket")
    flight_id: int = Field(..., description="ID of the flight")
    seat_class: str = Field(..., description="Seat class")
    price: str = Field(..., description="Ticket price")
    status: str = Field(..., description="Ticket status (should be 'reserved')")
    created_at: str = Field(..., description="Ticket creation timestamp")
    task_id: str = Field(..., description="Celery task ID for checkout session creation")
    message: str = Field(..., description="Informational message about the process")