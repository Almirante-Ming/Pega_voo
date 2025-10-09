from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Annotated, List
from http import HTTPStatus as HttpStatusCodes
import uuid

from app import schemas, models
from app.config.database import get_db
from app.config.auth import get_password_hash

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Annotated[Session, Depends(get_db)]):
    """Create a new usuario"""
    # Check if email or CPF already exists
    db_usuario_check = db.query(models.Usuario).filter(
        or_(
            models.Usuario.email == usuario.email,
            models.Usuario.cpf == usuario.cpf
        )
    ).first()
    
    if db_usuario_check:
        raise HTTPException(
            status_code=HttpStatusCodes.BAD_REQUEST, 
            detail="Email or CPF already registered."
        )
    
    # Hash the password
    usuario_data_dict = usuario.model_dump(exclude={"password"})
    hashed_password = get_password_hash(usuario.password)
    
    # Create new usuario
    new_usuario = models.Usuario(**usuario_data_dict, senha_hash=hashed_password)
    
    db.add(new_usuario)
    db.commit()
    db.refresh(new_usuario)
    return new_usuario


@router.get("/", response_model=List[schemas.Usuario])
def get_usuarios(db: Annotated[Session, Depends(get_db)]):
    """Get all usuarios"""
    return db.query(models.Usuario).filter(models.Usuario.deleted_at.is_(None)).all()


@router.get("/{usuario_id}", response_model=schemas.UsuarioComReservas)
def get_usuario(
    usuario_id: Annotated[str, Path(title="The ID of the usuario to retrieve")],
    db: Annotated[Session, Depends(get_db)]
):
    """Get a specific usuario by ID"""
    try:
        uuid_obj = uuid.UUID(usuario_id)
    except ValueError:
        raise HTTPException(
            status_code=HttpStatusCodes.BAD_REQUEST, 
            detail="Invalid UUID format"
        )
    
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == uuid_obj,
        models.Usuario.deleted_at.is_(None)
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Usuario not found"
        )
    return usuario


@router.get("/email/{email}", response_model=schemas.Usuario)
def get_usuario_by_email(
    email: Annotated[str, Path(title="The email of the usuario to retrieve")],
    db: Annotated[Session, Depends(get_db)]
):
    """Get a usuario by email"""
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == email,
        models.Usuario.deleted_at.is_(None)
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Usuario not found with this email"
        )
    return usuario


@router.put("/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(
    usuario_id: Annotated[str, Path(title="The ID of the usuario to update")],
    usuario_update: schemas.UsuarioUpdate,
    db: Annotated[Session, Depends(get_db)]
):
    """Update a usuario"""
    try:
        uuid_obj = uuid.UUID(usuario_id)
    except ValueError:
        raise HTTPException(
            status_code=HttpStatusCodes.BAD_REQUEST, 
            detail="Invalid UUID format"
        )
    
    db_usuario = db.query(models.Usuario).filter(
        models.Usuario.id == uuid_obj,
        models.Usuario.deleted_at.is_(None)
    ).first()
    
    if not db_usuario:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Usuario not found"
        )
    
    update_data = usuario_update.model_dump(exclude_unset=True)

    # Check if email is being updated and already exists
    if "email" in update_data and update_data["email"] != db_usuario.email:
        existing_email_check = db.query(models.Usuario).filter(
            models.Usuario.email == update_data["email"],
            models.Usuario.deleted_at.is_(None)
        ).first()
        if existing_email_check and existing_email_check.id != db_usuario.id:
            raise HTTPException(
                status_code=HttpStatusCodes.BAD_REQUEST, 
                detail="New email already registered by another user"
            )
    
    # Check if CPF is being updated and already exists
    if "cpf" in update_data and update_data["cpf"] != db_usuario.cpf:
        existing_cpf_check = db.query(models.Usuario).filter(
            models.Usuario.cpf == update_data["cpf"],
            models.Usuario.deleted_at.is_(None)
        ).first()
        if existing_cpf_check and existing_cpf_check.id != db_usuario.id:
            raise HTTPException(
                status_code=HttpStatusCodes.BAD_REQUEST, 
                detail="New CPF already registered by another user"
            )
    
    # Handle password update
    if "password" in update_data and update_data["password"] is not None:
        setattr(db_usuario, 'senha_hash', get_password_hash(update_data.pop("password")))

    # Update other fields
    for key, value in update_data.items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.delete("/{usuario_id}")
def delete_usuario(
    usuario_id: Annotated[str, Path(title="The ID of the usuario to delete")],
    db: Annotated[Session, Depends(get_db)]
):
    """Soft delete a usuario"""
    try:
        uuid_obj = uuid.UUID(usuario_id)
    except ValueError:
        raise HTTPException(
            status_code=HttpStatusCodes.BAD_REQUEST, 
            detail="Invalid UUID format"
        )
    
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == uuid_obj,
        models.Usuario.deleted_at.is_(None)
    ).first()
    
    if not usuario:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Usuario not found"
        )
    
    # Soft delete by setting deleted_at timestamp
    from datetime import datetime, UTC
    usuario.deleted_at = datetime.now(UTC)
    db.commit()
    return {"message": "Usuario deleted successfully"}