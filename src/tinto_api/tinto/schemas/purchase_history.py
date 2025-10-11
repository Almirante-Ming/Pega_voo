from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Any
from tinto.utils import Purchase_Status


class PurchaseHistoryBase(BaseModel):
    user_id: int = Field(..., description="Reference to user")
    status: Purchase_Status = Field(..., description="Purchase status")
    destiny: str = Field(..., description="Destination")
    origin: str = Field(..., description="Origin")

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v: Any) -> Purchase_Status:
        if isinstance(v, str):
            try:
                return Purchase_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Purchase_Status])}")
        return v


class PurchaseHistoryCreate(PurchaseHistoryBase):
    pass


class PurchaseHistoryUpdate(BaseModel):
    user_id: Optional[int] = None
    status: Optional[Purchase_Status] = None
    destiny: Optional[str] = None
    origin: Optional[str] = None

    @field_validator('status', mode='before')
    @classmethod
    def validate_status_update(cls, v: Any) -> Optional[Purchase_Status]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return Purchase_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Purchase_Status])}")
        return v


class PurchaseHistory(PurchaseHistoryBase):
    id: int
    dt_create: datetime
    dt_update: datetime

    model_config = {"from_attributes": True}