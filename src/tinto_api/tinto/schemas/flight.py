from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Any
from tinto.utils import Flight_Status, Flight_Class


class FlightBase(BaseModel):
    airline_id: int = Field(..., description="Reference to airline")
    flight_number: str = Field(..., description="Flight identifier")
    origin: str = Field(..., description="Origin airport/city")
    destiny: str = Field(..., description="Destination airport/city")
    f_class: Flight_Class = Field(default=Flight_Class.ECONOMY, description="Flight class")
    departure: datetime = Field(..., description="Scheduled departure time")
    arrival: datetime = Field(..., description="Scheduled arrival time")
    a_seats: int = Field(..., description="Available seat count")
    t_seats: int = Field(..., description="Total seat capacity")
    status: Flight_Status = Field(default=Flight_Status.SCHEDULED)

    @field_validator('f_class', mode='before')
    @classmethod
    def validate_f_class(cls, v: Any) -> Flight_Class:
        if isinstance(v, str):
            try:
                return Flight_Class(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Flight_Class])}")
        return v

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v: Any) -> Flight_Status:
        if isinstance(v, str):
            try:
                return Flight_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Flight_Status])}")
        return v


class FlightCreate(FlightBase):
    pass


class FlightUpdate(BaseModel):
    airline_id: Optional[int] = None
    flight_number: Optional[str] = None
    origin: Optional[str] = None
    destiny: Optional[str] = None
    f_class: Optional[Flight_Class] = None
    departure: Optional[datetime] = None
    arrival: Optional[datetime] = None
    a_seats: Optional[int] = None
    t_seats: Optional[int] = None
    status: Optional[Flight_Status] = None

    @field_validator('f_class', mode='before')
    @classmethod
    def validate_f_class_update(cls, v: Any) -> Optional[Flight_Class]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return Flight_Class(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Flight_Class])}")
        return v

    @field_validator('status', mode='before')
    @classmethod
    def validate_status_update(cls, v: Any) -> Optional[Flight_Status]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return Flight_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Flight_Status])}")
        return v


class Flight(FlightBase):
    id: int
    dt_create: datetime
    dt_update: datetime

    model_config = {"from_attributes": True}