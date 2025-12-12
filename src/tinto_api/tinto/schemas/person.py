from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime
from typing import Annotated, Optional, Any
from validate_docbr import CPF
from tinto.utils import User_Status, User_Type, Gender

def validate_cpf_util(value: str) -> str:
    digits = ''.join(filter(str.isdigit, value))
    if not CPF().validate(digits):
        raise ValueError(f"CPF inválido: {value}")
    return CPF().mask(digits)

class PersonBase(BaseModel):
    cpf: Annotated[str, Field(description="Valid CPF")]
    full_name: str
    email: EmailStr
    phone_number: str
    birth_date: str
    gender: Gender
    status: User_Status = Field(default=User_Status.ACTIVE)
    person_type: User_Type = Field(default=User_Type.CUSTOMER)
    password: Optional[str] = Field(None, description="User password")

    @field_validator("cpf")
    @classmethod
    def validate_cpf_format(cls, v: str) -> str:
        return validate_cpf_util(v)

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v: Any) -> User_Status:
        if isinstance(v, str):
            try:
                return User_Status(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in User_Status])}")
        return v

    @field_validator('person_type', mode='before')
    @classmethod
    def validate_person_type(cls, v: Any) -> User_Type:
        if isinstance(v, str):
            try:
                return User_Type(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in User_Type])}")
        return v

    @field_validator('gender', mode='before')
    @classmethod
    def validate_gender(cls, v: Any) -> Gender:
        if isinstance(v, str):
            try:
                return Gender(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Gender])}")
        return v

class PersonCreateInternal(PersonBase):
    password: str = Field(..., description="User password is required")

class PersonRegister(BaseModel):
    cpf: Annotated[str, Field(description="Valid CPF")]
    full_name: str
    email: EmailStr
    phone_number: str
    birth_date: str
    gender: Gender
    password: str = Field(..., description="User password is required")

    @field_validator("cpf")
    @classmethod
    def validate_cpf_format(cls, v: str) -> str:
        return validate_cpf_util(v)

    @field_validator('gender', mode='before')
    @classmethod
    def validate_gender(cls, v: Any) -> Gender:
        if isinstance(v, str):
            try:
                return Gender(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Gender])}")
        return v

class PersonUpdate(BaseModel):
    cpf: Optional[Annotated[str, Field(description="Valid CPF")]] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[Gender] = None
    status: Optional[User_Status] = None
    person_type: Optional[User_Type] = None
    password: Optional[str] = Field(None, description="New password (if changing)")

    @field_validator("cpf")
    @classmethod
    def validate_cpf_update_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None: return None
        return validate_cpf_util(v)

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

    @field_validator('person_type', mode='before')
    @classmethod
    def validate_person_type_update(cls, v: Any) -> Optional[User_Type]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return User_Type(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in User_Type])}")
        return v

    @field_validator('gender', mode='before')
    @classmethod
    def validate_gender_update(cls, v: Any) -> Optional[Gender]:
        if v is None: return None
        if isinstance(v, str):
            try:
                return Gender(v.lower())
            except ValueError:
                raise ValueError(f"Invalid value: '{v}'. Must be one of {', '.join([e.value for e in Gender])}")
        return v

class Person(PersonBase):
    id: int
    created_at: datetime
    updated_at: datetime
    password: Optional[str] = Field(None, exclude=True)

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    name: Optional[str] = None  
    user_id: Optional[int] = None
    acc_level: Optional[int] = None