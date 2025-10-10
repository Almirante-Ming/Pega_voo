from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.types import Enum as SqlEnum
from datetime import datetime, UTC
from tinto.utils import User_Status, User_Type

Base = declarative_base()
metadata = Base.metadata


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    dt_birth = Column(String, nullable=False)
    state = Column(SqlEnum(User_Status, name="user_status", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), default=User_Status.ACTIVE)
    p_type = Column(SqlEnum(User_Type, name="user_type", native_enum=False, values_callable=lambda obj: [e.value for e in obj]), default=User_Type.CUSTOMER)
    dt_create = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    dt_update = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
