from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime
from typing import Annotated, Optional, Any
from validate_docbr import CPF
from tinto.utils import User_Status, User_Type

def validate_cpf_util(value: str) -> str:
    digits = ''.join(filter(str.isdigit, value))
    if not CPF().validate(digits):
        raise ValueError(f"CPF inválido: {value}")
    return CPF().mask(digits)

class PersonBase(BaseModel):
    cpf: Annotated[str, Field(description="Valid CPF")]
    name: str
    email: EmailStr
    phone: str
    dt_birth: str
    state: User_Status = Field(default=User_Status.ACTIVE)
    p_type: User_Type = Field(default=User_Type.CUSTOMER)
    password: Optional[str] = Field(None, description="User password")

    @field_validator("cpf")
    @classmethod
    def validate_cpf_format(cls, v: str) -> str:
        return validate_cpf_util(v)

    @field_validator('state', mode='before')
    @classmethod
    def validate_state(cls, v: Any) -> User_Status:
        if isinstance(v, str):
            try:
                return User_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in User_Status])}")
        return v

    @field_validator('p_type', mode='before')
    @classmethod
    def validate_p_type(cls, v: Any) -> User_Type:
        if isinstance(v, str):
            try:
                return User_Type(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in User_Type])}")
        return v

class PersonCreateInternal(PersonBase):
    password: str = Field(..., description="User password is required")

class PersonRegister(BaseModel):
    cpf: Annotated[str, Field(description="Valid CPF")]
    name: str
    email: EmailStr
    phone: str
    dt_birth: str
    password: str = Field(..., description="User password is required")

    @field_validator("cpf")
    @classmethod
    def validate_cpf_format(cls, v: str) -> str:
        return validate_cpf_util(v)

class PersonUpdate(BaseModel):
    cpf: Optional[Annotated[str, Field(description="Valid CPF")]] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dt_birth: Optional[str] = None
    state: Optional[User_Status] = None
    p_type: Optional[User_Type] = None
    password: Optional[str] = Field(None, description="New password (if changing)")

    @field_validator("cpf")
    @classmethod
    def validate_cpf_update_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None: return None
        return validate_cpf_util(v)

    @field_validator('state', mode='before')
    @classmethod
    def validate_state_update(cls, v: Any) -> Optional[User_Status]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return User_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in User_Status])}")
        return v

    @field_validator('p_type', mode='before')
    @classmethod
    def validate_p_type_update(cls, v: Any) -> Optional[User_Type]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return User_Type(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in User_Type])}")
        return v

class Person(PersonBase):
    id: int
    dt_create: datetime
    dt_update: datetime
    password: Optional[str] = Field(None, exclude=True)

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    name: Optional[str] = None  
    user_id: Optional[int] = None
    acc_level: Optional[int] = None