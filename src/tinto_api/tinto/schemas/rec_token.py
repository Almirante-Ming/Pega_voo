from pydantic import BaseModel, EmailStr, field_validator, ValidationError, Field

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
    
class CodeCheckRequest(BaseModel):
    code: str = Field(..., description="Recovery code received by email")
class PasswordResetRequest(CodeCheckRequest):
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")
