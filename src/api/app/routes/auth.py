from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from app import schemas, models
from app.config.database import get_db
from app.config.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    """Login endpoint to get access token"""
    # Find user by email (username in form_data)
    user = db.query(models.Usuario).filter(
        models.Usuario.email == form_data.username,
        models.Usuario.deleted_at.is_(None)
    ).first()
    
    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.Usuario)
def register_user(
    user: schemas.UsuarioCreate, 
    db: Annotated[Session, Depends(get_db)]
):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(models.Usuario).filter(
        (models.Usuario.email == user.email) | (models.Usuario.cpf == user.cpf)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or CPF already exists"
        )
    
    # Create new user
    from app.config.auth import get_password_hash
    user_data = user.model_dump(exclude={"password"})
    hashed_password = get_password_hash(user.password)
    
    new_user = models.Usuario(**user_data, senha_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
    """Get current authenticated user"""
    from app.config.auth import verify_token
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = db.query(models.Usuario).filter(
        models.Usuario.email == email,
        models.Usuario.deleted_at.is_(None)
    ).first()
    
    if user is None:
        raise credentials_exception
    
    return user


@router.get("/me", response_model=schemas.UsuarioComReservas)
def read_users_me(
    current_user: Annotated[models.Usuario, Depends(get_current_user)]
):
    """Get current user info"""
    return current_user