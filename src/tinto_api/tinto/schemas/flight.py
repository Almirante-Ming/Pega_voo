from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Any, Dict
from tinto.utils import Flight_Status, Seat_Class, Booking_Status


class FlightBase(BaseModel):
    aircraft_model: str = Field(..., description="Aircraft model")
    flight_number: str = Field(..., description="Flight identifier")
    origin_city: str = Field(..., description="Origin city")
    origin_airport: str = Field(..., description="Origin airport IATA code")
    destination_city: str = Field(..., description="Destination city")
    destination_airport: str = Field(..., description="Destination airport IATA code")
    departure_time: datetime = Field(..., description="Scheduled departure time")
    estimated_arrival: datetime = Field(..., description="Scheduled arrival time")
    stops_count: int = Field(..., description="Total connection flights, 0 for direct")
    avaliable_seats: int = Field(...,description="Total of avaliable seats")
    premium_seats: int = Field(..., description="especial seats like as first, executive...")


class FlightCreateRequest(BaseModel):
    airline_id: int = Field(..., description="Reference to airline")
    aircraft_model: str = Field(..., description="Aircraft model")
    flight_number: str = Field(..., description="Flight identifier")
    origin_city: str = Field(..., description="Origin city")
    origin_airport: str = Field(..., description="Origin airport IATA code")
    destination_city: str = Field(..., description="Destination city")
    destination_airport: str = Field(..., description="Destination airport IATA code")
    departure_time: datetime = Field(..., description="Scheduled departure time")
    estimated_arrival: datetime = Field(..., description="Scheduled arrival time")
    stops_count: int = Field(..., description="Total connection flights, 0 for direct")
    avaliable_seats: int = Field(...,description="Total of avaliable seats")
    premium_seats: int = Field(..., description="especial seats like as first, executive...")
    economy_price: float = Field(..., description="Price for economy seats")
    premium_price: Optional[float] = Field(None, description="Price for premium seats (required if premium_seats > 0)")


class FlightCreate(FlightBase):
    airline_id: int = Field(..., description="Reference to airline")
    economy_price: float = Field(..., description="Price for economy seats")
    premium_price: Optional[float] = Field(None, description="Price for premium seats (required if premium_seats > 0)")
    status: Flight_Status = Field(default=Flight_Status.SCHEDULED)


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
    stops_count: Optional[int] = None
    premium_seats: Optional[int] = None
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
    airline_name: str = Field(..., description="Airline name")
    status: Flight_Status = Field(default=Flight_Status.SCHEDULED)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FlightWithSeatsAndPrices(FlightBase):
    """Flight response with prices by class"""
    id: int
    airline_name: str = Field(..., description="Airline name")
    status: Flight_Status = Field(default=Flight_Status.SCHEDULED)
    created_at: datetime
    updated_at: datetime
    tickets: Dict[str, float]  # key is seat_class (e.g., "economy", "premium"), value is price
    
    model_config = {"from_attributes": True}