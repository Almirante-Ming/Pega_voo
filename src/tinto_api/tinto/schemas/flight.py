from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Any
from tinto.utils import Flight_Status


class FlightBase(BaseModel):
    airline_id: int = Field(..., description="Reference to airline")
    aircraft_model: str = Field(..., description="Aircraft model")
    flight_number: str = Field(..., description="Flight identifier")
    origin_city: str = Field(..., description="Origin city")
    origin_airport: str = Field(..., description="Origin airport IATA code")
    destination_city: str = Field(..., description="Destination city")
    destination_airport: str = Field(..., description="Destination airport IATA code")
    departure_time: datetime = Field(..., description="Scheduled departure time")
    estimated_arrival: datetime = Field(..., description="Scheduled arrival time")
    economy_seats: int = Field(..., description="Total economy seats")
    business_seats: int = Field(..., description="Total business seats")
    first_seats: int = Field(..., description="Total first class seats")
    status: Flight_Status = Field(default=Flight_Status.SCHEDULED)

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
    aircraft_model: Optional[str] = None
    flight_number: Optional[str] = None
    origin_city: Optional[str] = None
    origin_airport: Optional[str] = None
    destination_city: Optional[str] = None
    destination_airport: Optional[str] = None
    departure_time: Optional[datetime] = None
    estimated_arrival: Optional[datetime] = None
    economy_seats: Optional[int] = None
    business_seats: Optional[int] = None
    first_seats: Optional[int] = None
    status: Optional[Flight_Status] = None

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
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}