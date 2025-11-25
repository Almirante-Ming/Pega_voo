from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Any
from decimal import Decimal
from tinto.utils import Booking_Status, Seat_Class


class TicketBase(BaseModel):
    flight_id: int = Field(..., description="Reference to flight")
    passenger_id: int = Field(..., description="Reference to passenger (person)")
    seat_class: Seat_Class = Field(..., description="Seat class")
    seat_number: Optional[str] = Field(None, description="Seat number")
    price: Decimal = Field(..., description="Ticket price")
    boarding_time: datetime = Field(..., description="Boarding time")
    arrival_time: datetime = Field(..., description="Arrival time")
    status: Booking_Status = Field(default=Booking_Status.MARKED)

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v: Any) -> Booking_Status:
        if isinstance(v, str):
            try:
                return Booking_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Booking_Status])}")
        return v

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
    seat_class: Seat_Class = Field(..., description="Seat class")
    seat_number: Optional[str] = Field(None, description="Seat number")
    price: Decimal = Field(..., description="Ticket price")
    boarding_time: datetime = Field(..., description="Boarding time")
    arrival_time: datetime = Field(..., description="Arrival time")
    status: Booking_Status = Field(default=Booking_Status.MARKED)

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v: Any) -> Booking_Status:
        if isinstance(v, str):
            try:
                return Booking_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Booking_Status])}")
        return v

    @field_validator('seat_class', mode='before')
    @classmethod
    def validate_seat_class(cls, v: Any) -> Seat_Class:
        if isinstance(v, str):
            try:
                return Seat_Class(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Seat_Class])}")
        return v


class TicketUpdate(BaseModel):
    flight_id: Optional[int] = None
    passenger_id: Optional[int] = None
    seat_class: Optional[Seat_Class] = None
    seat_number: Optional[str] = None
    price: Optional[Decimal] = None
    boarding_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    status: Optional[Booking_Status] = None

    @field_validator('status', mode='before')
    @classmethod
    def validate_status_update(cls, v: Any) -> Optional[Booking_Status]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return Booking_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Booking_Status])}")
        return v

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