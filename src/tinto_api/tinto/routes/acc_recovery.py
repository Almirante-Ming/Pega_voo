from fastapi import APIRouter, HTTPException, status
from sqlalchemy import or_
from pydantic import BaseModel, EmailStr, field_validator, ValidationError, Field
from datetime import datetime, timedelta, UTC
from typing import Dict

from tinto.models import Person
from tinto.utils import send_mail, DBSession, kcode, get_password_hash, verify_password

router = APIRouter(tags=['access recovery'])

# use redis after implement celery jobs
recovery_codes_store: Dict[str, dict] = {}

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
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with provided identifier"
        )
    
    # Using getattr to avoid type checker issues with SQLAlchemy models
    user_id = getattr(user, 'id', None)
    if user_id == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account recovery not available for this user"
        )
    
    expire_time = datetime.now(UTC) + timedelta(minutes=5)
    
    # will be send on redis after jobs 
    recovery_codes_store[kcode] = {
        "code": kcode,
        "user": user.email,
        "expire_time": expire_time.timestamp()
    }
    
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
    
    if code not in recovery_codes_store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid recovery code"
        )
    
    code_data = recovery_codes_store[code]
    
    current_time = datetime.now(UTC).timestamp()
    if current_time > code_data["expire_time"]:
        del recovery_codes_store[code]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expired token"
        )
    
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
    
    del recovery_codes_store[code]
    
    return {"message": "Password reset successfully","status_code":status.HTTP_200_OK}