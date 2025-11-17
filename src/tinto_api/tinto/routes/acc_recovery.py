from fastapi import APIRouter, HTTPException, status
from sqlalchemy import or_
from datetime import datetime, UTC
from tinto.models import Person
from tinto.utils import send_mail, DBSession, kcode, get_password_hash, verify_password, minerva
from tinto.schemas import RecoveryRequest, PasswordResetRequest, CodeCheckRequest
import json


router = APIRouter(tags=['Access Recovery'])



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
    def format_cpf(cpf: str) -> str:
        cpf_digits = ''.join(filter(str.isdigit, cpf))
        return f"{cpf_digits[:2]}*.***.**{cpf_digits[8]}-{cpf_digits[9:]}"
        

    
    return {
        "message": "Recovery code sent successfully",
        "redirect": "/auth2r",
        "user_info": {
            "fullname": user.full_name,
            "cpf": format_cpf(str(user.cpf))
        }
    }



@router.post('/chkCode', status_code=status.HTTP_200_OK)
def check_code(request: CodeCheckRequest):
    code = request.code.strip()
    recovery_key = f"recovery:{code}"

    try:
        raw = minerva.get(recovery_key)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if not raw:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired recovery code")

    return {}

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