from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Any, List, Dict
from decimal import Decimal
from tinto.utils import Booking_Status
import json


class TicketBase(BaseModel):
    purchase_history_id: int = Field(..., description="Reference to purchase history")
    flight_id: int = Field(..., description="Reference to flight")
    passengers: str = Field(..., description="JSON string with passenger information")
    valor: Decimal = Field(..., description="Ticket price")
    horario_embarque: datetime = Field(..., description="Boarding time")
    horario_desembarque: datetime = Field(..., description="Arrival time")
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

    @field_validator('passengers', mode='before')
    @classmethod
    def validate_passengers(cls, v: Any) -> str:
        if isinstance(v, (list, dict)):
            return json.dumps(v)
        if isinstance(v, str):
            # Validate it's valid JSON
            try:
                json.loads(v)
                return v
            except json.JSONDecodeError:
                raise ValueError("Passengers must be valid JSON")
        raise ValueError("Passengers must be a JSON string, list, or dict")


class TicketCreate(TicketBase):
    pass


class TicketCreateWithPassengerList(BaseModel):
    purchase_history_id: int = Field(..., description="Reference to purchase history")
    flight_id: int = Field(..., description="Reference to flight")
    passengers: List[Dict] = Field(..., description="List of passenger information")
    valor: Decimal = Field(..., description="Ticket price")
    horario_embarque: datetime = Field(..., description="Boarding time")
    horario_desembarque: datetime = Field(..., description="Arrival time")
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


class TicketUpdate(BaseModel):
    purchase_history_id: Optional[int] = None
    flight_id: Optional[int] = None
    passengers: Optional[str] = None
    valor: Optional[Decimal] = None
    horario_embarque: Optional[datetime] = None
    horario_desembarque: Optional[datetime] = None
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

    @field_validator('passengers', mode='before')
    @classmethod
    def validate_passengers_update(cls, v: Any) -> Optional[str]:
        if v is None: return None
        if isinstance(v, (list, dict)):
            return json.dumps(v)
        if isinstance(v, str):
            try:
                json.loads(v)
                return v
            except json.JSONDecodeError:
                raise ValueError("Passengers must be valid JSON")
        raise ValueError("Passengers must be a JSON string, list, or dict")


class Ticket(TicketBase):
    id: int
    dt_create: datetime
    dt_update: datetime

    model_config = {"from_attributes": True}


class TicketWithParsedPassengers(BaseModel):
    id: int
    purchase_history_id: int
    flight_id: int
    passengers: List[Dict] = Field(..., description="Parsed passenger information")
    valor: Decimal
    horario_embarque: datetime
    horario_desembarque: datetime
    status: Booking_Status
    dt_create: datetime
    dt_update: datetime

    model_config = {"from_attributes": True}