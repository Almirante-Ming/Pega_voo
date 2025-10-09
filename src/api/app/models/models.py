from sqlalchemy import Column, String, DateTime, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.types import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, UTC
from enum import Enum
import uuid

Base = declarative_base()
metadata = Base.metadata


class TierPassagem(Enum):
    """Enum for flight ticket tiers"""
    ECONOMICA = "economica"
    EXECUTIVA = "executiva"
    PRIMEIRA_CLASSE = "primeira_classe"


class StatusReserva(Enum):
    """Enum for reservation status"""
    ATIVA = "ativa"
    CANCELADA = "cancelada"
    CONFIRMADA = "confirmada"
    PENDENTE = "pendente"


class Usuario(Base):
    """Usuario (User) table"""
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome_completo = Column(String(150), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    genero = Column(String(20), nullable=True)
    telefone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String, nullable=True)
    origem_cadastro = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    reservas = relationship("Reserva", back_populates="usuario")


class Voo(Base):
    """Voo (Flight) table"""
    __tablename__ = "voos"

    id_voo = Column(Integer, primary_key=True, autoincrement=True, index=True)
    numero_voo = Column(String(20), nullable=False)
    origem = Column(String(10), nullable=False)
    destino = Column(String(10), nullable=False)
    data_ida = Column(Date, nullable=False)
    companhia_aerea = Column(String(100), nullable=False)
    tier = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    reservas = relationship("Reserva", back_populates="voo")

    @property
    def tier_enum(self) -> TierPassagem:
        """Get tier as enum"""
        return TierPassagem(self.tier)

    @tier_enum.setter
    def tier_enum(self, value: TierPassagem):
        """Set tier from enum"""
        self.tier = value.value


class Reserva(Base):
    """Reserva (Reservation) table"""
    __tablename__ = "reservas"

    id_reserva = Column(String(20), primary_key=True, index=True)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    id_voo = Column(Integer, ForeignKey("voos.id_voo"), nullable=False)
    data_reserva = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    status = Column(String(20), default=StatusReserva.ATIVA.value)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    usuario = relationship("Usuario", back_populates="reservas")
    voo = relationship("Voo", back_populates="reservas")

    @property
    def status_enum(self) -> StatusReserva:
        """Get status as enum"""
        return StatusReserva(self.status)

    @status_enum.setter
    def status_enum(self, value: StatusReserva):
        """Set status from enum"""
        self.status = value.value