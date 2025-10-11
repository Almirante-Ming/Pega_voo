from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Any
from tinto.utils import User_Status


class AirlineBase(BaseModel):
    name: str = Field(..., description="Airline name")
    code: str = Field(..., description="IATA/ICAO airline code")
    country: str = Field(..., description="Country of origin")
    status: User_Status = Field(default=User_Status.ACTIVE)

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v: Any) -> User_Status:
        if isinstance(v, str):
            try:
                return User_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in User_Status])}")
        return v


class AirlineCreate(AirlineBase):
    pass


class AirlineUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    country: Optional[str] = None
    status: Optional[User_Status] = None

    @field_validator('status', mode='before')
    @classmethod
    def validate_status_update(cls, v: Any) -> Optional[User_Status]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return User_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in User_Status])}")
        return v


class Airline(AirlineBase):
    id: int
    dt_create: datetime
    dt_update: datetime

    model_config = {"from_attributes": True}