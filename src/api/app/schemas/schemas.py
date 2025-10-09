from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict
from datetime import datetime, date
from typing import Annotated, Optional, Any, List
from validate_docbr import CPF
from app.models.models import TierPassagem, StatusReserva
import uuid


def validate_cpf_util(value: str) -> str:
    """Validate and format CPF"""
    digits = ''.join(filter(str.isdigit, value))
    if not CPF().validate(digits):
        raise ValueError(f"CPF inválido: {value}")
    return CPF().mask(digits)


# Usuario schemas
class UsuarioBase(BaseModel):
    """Base schema for Usuario"""
    nome_completo: str = Field(..., max_length=150, description="Full name")
    cpf: Annotated[str, Field(description="Valid CPF")]
    data_nascimento: date = Field(..., description="Birth date")
    genero: Optional[str] = Field(None, max_length=20, description="Gender")
    telefone: str = Field(..., max_length=20, description="Phone number")
    email: EmailStr = Field(..., max_length=100, description="Email address")
    origem_cadastro: Optional[str] = Field(None, max_length=20, description="Registration origin")
    password: Optional[str] = Field(None, description="User password")

    @field_validator("cpf")
    @classmethod
    def validate_cpf_format(cls, v: str) -> str:
        return validate_cpf_util(v)


class UsuarioCreate(UsuarioBase):
    """Schema for creating a new Usuario"""
    password: str = Field(..., description="User password is required")


class UsuarioUpdate(BaseModel):
    """Schema for updating an existing Usuario"""
    nome_completo: Optional[str] = Field(None, max_length=150)
    cpf: Optional[Annotated[str, Field(description="Valid CPF")]] = None
    data_nascimento: Optional[date] = None
    genero: Optional[str] = Field(None, max_length=20)
    telefone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = Field(None, max_length=100)
    origem_cadastro: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, description="New password (if changing)")

    @field_validator("cpf")
    @classmethod
    def validate_cpf_update_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None: 
            return None
        return validate_cpf_util(v)


class Usuario(UsuarioBase):
    """Response schema for Usuario"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    password: Optional[str] = Field(None, exclude=True)

    model_config = ConfigDict(from_attributes=True)


# Voo schemas
class VooBase(BaseModel):
    """Base schema for Voo"""
    numero_voo: str = Field(..., max_length=20, description="Flight number")
    origem: str = Field(..., max_length=10, description="Origin airport code")
    destino: str = Field(..., max_length=10, description="Destination airport code")
    data_ida: date = Field(..., description="Departure date")
    companhia_aerea: str = Field(..., max_length=100, description="Airline company")
    tier: TierPassagem = Field(..., description="Flight tier")

    @field_validator('tier', mode='before')
    @classmethod
    def validate_tier(cls, v: Any) -> TierPassagem:
        if isinstance(v, str):
            try:
                return TierPassagem(v.lower())
            except ValueError:
                raise ValueError(f"Invalid tier: '{v}'. Must be one of {', '.join([e.value for e in TierPassagem])}")
        return v


class VooCreate(VooBase):
    """Schema for creating a new Voo"""
    pass


class VooUpdate(BaseModel):
    """Schema for updating an existing Voo"""
    numero_voo: Optional[str] = Field(None, max_length=20)
    origem: Optional[str] = Field(None, max_length=10)
    destino: Optional[str] = Field(None, max_length=10)
    data_ida: Optional[date] = None
    companhia_aerea: Optional[str] = Field(None, max_length=100)
    tier: Optional[TierPassagem] = None

    @field_validator('tier', mode='before')
    @classmethod
    def validate_tier_update(cls, v: Any) -> Optional[TierPassagem]:
        if v is None: 
            return None
        if isinstance(v, str):
            try:
                return TierPassagem(v.lower())
            except ValueError:
                raise ValueError(f"Invalid tier: '{v}'. Must be one of {', '.join([e.value for e in TierPassagem])}")
        return v


class Voo(VooBase):
    """Response schema for Voo"""
    id_voo: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj, *, strict=None, from_attributes=None, context=None):
        """Custom model_validate to handle enum conversion for Pydantic v2"""
        if from_attributes and hasattr(obj, '__dict__'):
            data = {
                "id_voo": obj.id_voo,
                "numero_voo": obj.numero_voo,
                "origem": obj.origem,
                "destino": obj.destino,
                "data_ida": obj.data_ida,
                "companhia_aerea": obj.companhia_aerea,
                "tier": TierPassagem(obj.tier),  # Convert string to enum
                "created_at": obj.created_at,
                "updated_at": obj.updated_at,
                "deleted_at": obj.deleted_at,
            }
            return cls.model_validate(data, strict=strict, context=context)
        return super().model_validate(obj, strict=strict, from_attributes=from_attributes, context=context)
    
    @classmethod
    def from_orm(cls, obj):
        """Backward compatibility method"""
        return cls.model_validate(obj, from_attributes=True)


# Reserva schemas
class ReservaBase(BaseModel):
    """Base schema for Reserva"""
    id_reserva: str = Field(..., max_length=20, description="Reservation ID")
    id_usuario: uuid.UUID = Field(..., description="User ID")
    id_voo: int = Field(..., description="Flight ID")
    data_reserva: Optional[datetime] = Field(None, description="Reservation date")
    status: StatusReserva = Field(default=StatusReserva.ATIVA, description="Reservation status")

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v: Any) -> StatusReserva:
        if isinstance(v, str):
            try:
                return StatusReserva(v.lower())
            except ValueError:
                raise ValueError(f"Invalid status: '{v}'. Must be one of {', '.join([e.value for e in StatusReserva])}")
        return v


class ReservaCreate(ReservaBase):
    """Schema for creating a new Reserva"""
    pass


class ReservaUpdate(BaseModel):
    """Schema for updating an existing Reserva"""
    id_usuario: Optional[uuid.UUID] = None
    id_voo: Optional[int] = None
    data_reserva: Optional[datetime] = None
    status: Optional[StatusReserva] = None

    @field_validator('status', mode='before')
    @classmethod
    def validate_status_update(cls, v: Any) -> Optional[StatusReserva]:
        if v is None: 
            return None
        if isinstance(v, str):
            try:
                return StatusReserva(v.lower())
            except ValueError:
                raise ValueError(f"Invalid status: '{v}'. Must be one of {', '.join([e.value for e in StatusReserva])}")
        return v


class Reserva(ReservaBase):
    """Response schema for Reserva"""
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj, *, strict=None, from_attributes=None, context=None):
        """Custom model_validate to handle enum conversion for Pydantic v2"""
        if from_attributes and hasattr(obj, '__dict__'):
            data = {
                "id_reserva": obj.id_reserva,
                "id_usuario": obj.id_usuario,
                "id_voo": obj.id_voo,
                "data_reserva": obj.data_reserva,
                "status": StatusReserva(obj.status),  # Convert string to enum
                "created_at": obj.created_at,
                "updated_at": obj.updated_at,
                "deleted_at": obj.deleted_at,
            }
            return cls.model_validate(data, strict=strict, context=context)
        return super().model_validate(obj, strict=strict, from_attributes=from_attributes, context=context)
    
    @classmethod
    def from_orm(cls, obj):
        """Backward compatibility method"""
        return cls.model_validate(obj, from_attributes=True)


# Combined schemas for detailed responses
class ReservaDetalhada(ReservaBase):
    """Detailed Reserva response with Usuario and Voo information"""
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    usuario: Usuario
    voo: Voo

    model_config = ConfigDict(from_attributes=True)


class UsuarioComReservas(Usuario):
    """Usuario response with reservations list"""
    reservas: List[Reserva] = []

    model_config = ConfigDict(from_attributes=True)


class VooComReservas(Voo):
    """Voo response with reservations list"""
    reservas: List[Reserva] = []

    model_config = ConfigDict(from_attributes=True)


# Authentication schemas
class Token(BaseModel):
    """Token schema for authentication"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema"""
    email: Optional[str] = None
    user_id: Optional[uuid.UUID] = None