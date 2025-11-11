from pydantic import BaseModel, EmailStr

class RecToken(BaseModel):
    email: EmailStr
    code: str
    used: bool
    
    