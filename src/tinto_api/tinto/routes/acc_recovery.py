from fastapi import APIRouter, HTTPException, status
from redis import Redis
from sqlalchemy import or_
from pydantic import BaseModel, EmailStr, field_validator, ValidationError, Field
from datetime import datetime, timedelta, UTC
from typing import Optional
import json

from tinto.models import Person
from tinto.utils import send_mail, DBSession, kcode, get_password_hash, verify_password

import os

router = APIRouter(tags=['access recovery'])

minerva = Redis(host=str(os.getenv('CELERY_HOST')), port=30059, password=str(os.getenv('CELERY_PASS')))

class RecoveryRequest(BaseModel):
    identifier: str
    
    @field_validator('identifier')
    @classmethod
    def validate_identifier(cls, v: str) -> str:
        v = v.strip()

        try:
            class EmailValidator(BaseModel):
                email: EmailStr
            
            EmailValidator(email=v)
            return v
        
        except ValidationError:
            pass 
        
        if len(v) == 11 and v.isdigit():
            try:
                int(v)
                return v
            
            except ValueError:
                pass
        
        raise ValueError("Invalid identifier")

@router.post('/recovery', status_code=status.HTTP_200_OK)
def get_recovery_code(form_data: RecoveryRequest, db: DBSession):
    identifier = form_data.identifier
    
    user = db.query(Person).filter(
        or_(
            Person.email == identifier,
            Person.phone_number == identifier
        )
    ).first()
    
    # Using getattr to avoid type checker issues with SQLAlchemy models
    user_id = getattr(user, 'id', None)
    
    if not user or user_id == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with provided identifier"
        )
    
    expire_time = datetime.now(UTC) + timedelta(minutes=5)
    
    recovery_key = f"recovery:{kcode}"
    payload = {"code": kcode, "user": user.email}
    try:
        # ex == expiration
        result = minerva.set(recovery_key, json.dumps(payload), ex=600)
        if not result:
            raise RuntimeError("Failed to set key")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    try:
        send_mail(user.email, kcode)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email: {str(e)}"
        )
    
    return {
        "message": "Recovery code sent successfully",
        "redirect": "/auth2r"
    }


class PasswordResetRequest(BaseModel):
    code: str = Field(..., description="Recovery code received by email")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")


@router.post('/auth2r', status_code=status.HTTP_200_OK)
def verify_recovery_code(reset_request: PasswordResetRequest, db: DBSession):
    code = reset_request.code.strip()
    new_password = reset_request.new_password
    
    recovery_key = f"recovery:{code}"

    try:
        raw = minerva.get(recovery_key)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if not raw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired recovery code")

    # Redis may return bytes or other types; coerce to str then load JSON
    if isinstance(raw, (bytes, bytearray)):
        decoded = raw.decode('utf-8')
    else:
        decoded = str(raw)
    try:
        code_data = json.loads(decoded)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    user_email = code_data["user"]
    
    user = db.query(Person).filter(Person.email == user_email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    current_hashed_password = getattr(user, 'hashed_password', None)
    if current_hashed_password and verify_password(new_password, current_hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )
    
    hashed_password = get_password_hash(new_password)
    
    user.hashed_password = hashed_password  # type: ignore
    user.updated_at = datetime.now(UTC)  # type: ignore
    

    db.commit()
    db.refresh(user)
    
    try:
        minerva.delete(recovery_key)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"message": "Password reset successfully","status_code":status.HTTP_200_OK}