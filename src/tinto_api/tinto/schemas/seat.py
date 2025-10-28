from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from tinto.utils import Seat_Class


class SeatBase(BaseModel):
    flight_id: int = Field(..., description="Reference to flight")
    seat_number: str = Field(..., description="Seat number (e.g., 12A)")
    seat_class: Seat_Class = Field(..., description="Seat class")
    is_available: bool = Field(default=True, description="Seat availability")
    ticket_id: Optional[int] = Field(None, description="Reference to ticket if occupied")

    @field_validator('seat_class', mode='before')
    @classmethod
    def validate_seat_class(cls, v: Any) -> Seat_Class:
        if isinstance(v, str):
            try:
                return Seat_Class(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Seat_Class])}")
        return v


class SeatCreate(SeatBase):
    pass


class SeatUpdate(BaseModel):
    flight_id: Optional[int] = None
    seat_number: Optional[str] = None
    seat_class: Optional[Seat_Class] = None
    is_available: Optional[bool] = None
    ticket_id: Optional[int] = None

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


class Seat(SeatBase):
    id: int

    model_config = {"from_attributes": True}
