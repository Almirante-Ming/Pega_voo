from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Any
from decimal import Decimal
from tinto.utils import Purchase_Status, Payment_Method


class PurchaseHistoryBase(BaseModel):
    person_id: int = Field(..., description="Reference to person")
    status: Purchase_Status = Field(..., description="Purchase status")
    total_amount: Decimal = Field(..., description="Total purchase amount")
    payment_method: Payment_Method = Field(..., description="Payment method")

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v: Any) -> Purchase_Status:
        if isinstance(v, str):
            try:
                return Purchase_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Purchase_Status])}")
        return v

    @field_validator('payment_method', mode='before')
    @classmethod
    def validate_payment_method(cls, v: Any) -> Payment_Method:
        if isinstance(v, str):
            try:
                return Payment_Method(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Payment_Method])}")
        return v


class PurchaseHistoryCreate(PurchaseHistoryBase):
    pass


class PurchaseHistoryUpdate(BaseModel):
    person_id: Optional[int] = None
    status: Optional[Purchase_Status] = None
    total_amount: Optional[Decimal] = None
    payment_method: Optional[Payment_Method] = None

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

    @field_validator('payment_method', mode='before')
    @classmethod
    def validate_payment_method_update(cls, v: Any) -> Optional[Payment_Method]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return Payment_Method(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Payment_Method])}")
        return v


class PurchaseHistory(PurchaseHistoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}