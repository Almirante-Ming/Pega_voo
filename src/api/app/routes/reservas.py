from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Annotated, List, Optional
from http import HTTPStatus as HttpStatusCodes
import uuid

from app import schemas, models
from app.config.database import get_db

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("/", response_model=schemas.Reserva)
def create_reserva(reserva: schemas.ReservaCreate, db: Annotated[Session, Depends(get_db)]):
    """Create a new reserva (reservation)"""
    # Check if usuario exists
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == reserva.id_usuario,
        models.Usuario.deleted_at.is_(None)
    ).first()
    if not usuario:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail=f"Usuario with id {reserva.id_usuario} not found"
        )
    
    # Check if voo exists
    voo = db.query(models.Voo).filter(
        models.Voo.id_voo == reserva.id_voo,
        models.Voo.deleted_at.is_(None)
    ).first()
    if not voo:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail=f"Voo with id {reserva.id_voo} not found"
        )
    
    # Check if reservation ID already exists
    existing_reserva = db.query(models.Reserva).filter(
        models.Reserva.id_reserva == reserva.id_reserva,
        models.Reserva.deleted_at.is_(None)
    ).first()
    if existing_reserva:
        raise HTTPException(
            status_code=HttpStatusCodes.BAD_REQUEST,
            detail=f"Reservation with id {reserva.id_reserva} already exists"
        )
    
    reserva_data = reserva.model_dump()
    # Convert enum to string for database storage
    reserva_data["status"] = reserva_data["status"].value
    
    new_reserva = models.Reserva(**reserva_data)
    db.add(new_reserva)
    db.commit()
    db.refresh(new_reserva)
    return schemas.Reserva.model_validate(new_reserva, from_attributes=True)


@router.get("/", response_model=List[schemas.ReservaDetalhada])
def get_reservas(
    usuario_id: Annotated[Optional[str], Query(description="Filter by usuario ID")] = None,
    voo_id: Annotated[Optional[int], Query(description="Filter by voo ID")] = None,
    status: Annotated[Optional[str], Query(description="Filter by status")] = None,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Get all reservas with optional filters"""
    query = db.query(models.Reserva).options(
        joinedload(models.Reserva.usuario),
        joinedload(models.Reserva.voo)
    ).filter(models.Reserva.deleted_at.is_(None))
    
    if usuario_id:
        try:
            uuid_obj = uuid.UUID(usuario_id)
            query = query.filter(models.Reserva.id_usuario == uuid_obj)
        except ValueError:
            raise HTTPException(
                status_code=HttpStatusCodes.BAD_REQUEST,
                detail="Invalid UUID format for usuario_id"
            )
    
    if voo_id:
        query = query.filter(models.Reserva.id_voo == voo_id)
    
    if status:
        try:
            # Filter by string value directly since we store as string
            query = query.filter(models.Reserva.status == status.lower())
        except ValueError:
            raise HTTPException(
                status_code=HttpStatusCodes.BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join([e.value for e in models.StatusReserva])}"
            )
    
    return query.all()


@router.get("/{reserva_id}", response_model=schemas.ReservaDetalhada)
def get_reserva(reserva_id: str, db: Annotated[Session, Depends(get_db)]):
    """Get a specific reserva by ID"""
    reserva = db.query(models.Reserva).options(
        joinedload(models.Reserva.usuario),
        joinedload(models.Reserva.voo)
    ).filter(
        models.Reserva.id_reserva == reserva_id,
        models.Reserva.deleted_at.is_(None)
    ).first()
    
    if not reserva:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Reserva not found"
        )
    return reserva


@router.get("/usuario/{usuario_id}", response_model=List[schemas.ReservaDetalhada])
def get_reservas_by_usuario(
    usuario_id: str, 
    db: Annotated[Session, Depends(get_db)]
):
    """Get all reservas for a specific usuario"""
    try:
        uuid_obj = uuid.UUID(usuario_id)
    except ValueError:
        raise HTTPException(
            status_code=HttpStatusCodes.BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    # Check if usuario exists
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == uuid_obj,
        models.Usuario.deleted_at.is_(None)
    ).first()
    if not usuario:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND,
            detail="Usuario not found"
        )
    
    reservas = db.query(models.Reserva).options(
        joinedload(models.Reserva.usuario),
        joinedload(models.Reserva.voo)
    ).filter(
        models.Reserva.id_usuario == uuid_obj,
        models.Reserva.deleted_at.is_(None)
    ).all()
    
    return reservas


@router.put("/{reserva_id}", response_model=schemas.Reserva)
def update_reserva(
    reserva_id: str, 
    reserva_update: schemas.ReservaUpdate, 
    db: Annotated[Session, Depends(get_db)]
):
    """Update a reserva"""
    db_reserva = db.query(models.Reserva).filter(
        models.Reserva.id_reserva == reserva_id,
        models.Reserva.deleted_at.is_(None)
    ).first()
    
    if not db_reserva:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Reserva not found"
        )
    
    update_data = reserva_update.model_dump(exclude_unset=True)
    
    # Validate usuario if being updated
    if "id_usuario" in update_data:
        usuario = db.query(models.Usuario).filter(
            models.Usuario.id == update_data["id_usuario"],
            models.Usuario.deleted_at.is_(None)
        ).first()
        if not usuario:
            raise HTTPException(
                status_code=HttpStatusCodes.NOT_FOUND,
                detail=f"Usuario with id {update_data['id_usuario']} not found"
            )
    
    # Validate voo if being updated
    if "id_voo" in update_data:
        voo = db.query(models.Voo).filter(
            models.Voo.id_voo == update_data["id_voo"],
            models.Voo.deleted_at.is_(None)
        ).first()
        if not voo:
            raise HTTPException(
                status_code=HttpStatusCodes.NOT_FOUND,
                detail=f"Voo with id {update_data['id_voo']} not found"
            )
    
    # Convert enum to string for database storage
    if "status" in update_data and update_data["status"] is not None:
        update_data["status"] = update_data["status"].value
    
    for key, value in update_data.items():
        setattr(db_reserva, key, value)
    
    db.commit()
    db.refresh(db_reserva)
    return schemas.Reserva.model_validate(db_reserva, from_attributes=True)


@router.delete("/{reserva_id}")
def delete_reserva(reserva_id: str, db: Annotated[Session, Depends(get_db)]):
    """Soft delete a reserva"""
    reserva = db.query(models.Reserva).filter(
        models.Reserva.id_reserva == reserva_id,
        models.Reserva.deleted_at.is_(None)
    ).first()
    
    if not reserva:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Reserva not found"
        )
    
    # Soft delete by setting deleted_at timestamp
    from datetime import datetime, UTC
    reserva.deleted_at = datetime.now(UTC)
    db.commit()
    return {"message": "Reserva deleted successfully"}


@router.post("/{reserva_id}/cancel")
def cancel_reserva(reserva_id: str, db: Annotated[Session, Depends(get_db)]):
    """Cancel a reserva by changing its status"""
    reserva = db.query(models.Reserva).filter(
        models.Reserva.id_reserva == reserva_id,
        models.Reserva.deleted_at.is_(None)
    ).first()
    
    if not reserva:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Reserva not found"
        )
    
    if reserva.status == models.StatusReserva.CANCELADA.value:
        raise HTTPException(
            status_code=HttpStatusCodes.BAD_REQUEST,
            detail="Reserva is already cancelled"
        )
    
    reserva.status = models.StatusReserva.CANCELADA.value
    db.commit()
    return {"message": "Reserva cancelled successfully"}


@router.post("/{reserva_id}/confirm")
def confirm_reserva(reserva_id: str, db: Annotated[Session, Depends(get_db)]):
    """Confirm a reserva by changing its status"""
    reserva = db.query(models.Reserva).filter(
        models.Reserva.id_reserva == reserva_id,
        models.Reserva.deleted_at.is_(None)
    ).first()
    
    if not reserva:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Reserva not found"
        )
    
    if reserva.status == models.StatusReserva.CONFIRMADA.value:
        raise HTTPException(
            status_code=HttpStatusCodes.BAD_REQUEST,
            detail="Reserva is already confirmed"
        )
    
    if reserva.status == models.StatusReserva.CANCELADA.value:
        raise HTTPException(
            status_code=HttpStatusCodes.BAD_REQUEST,
            detail="Cannot confirm a cancelled reservation"
        )
    
    reserva.status = models.StatusReserva.CONFIRMADA.value
    db.commit()
    return {"message": "Reserva confirmed successfully"}