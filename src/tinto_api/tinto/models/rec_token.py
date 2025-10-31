from tinto.utils import Base
from sqlalchemy import Column, Integer, Boolean, String, DateTime
from datetime import datetime, UTC

class OTPCode(Base):
    __tablename__ = "otp_codes"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    code = Column(String, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    expires_at = Column(DateTime)