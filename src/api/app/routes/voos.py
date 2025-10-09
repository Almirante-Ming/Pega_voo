from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional
from http import HTTPStatus as HttpStatusCodes
from datetime import date

from app import schemas, models
from app.config.database import get_db

router = APIRouter(prefix="/voos", tags=["Voos"])


@router.post("/", response_model=schemas.Voo)
def create_voo(voo: schemas.VooCreate, db: Annotated[Session, Depends(get_db)]):
    """Create a new voo (flight)"""
    voo_data = voo.model_dump()
    # Convert enum to string for database storage
    voo_data["tier"] = voo_data["tier"].value
    
    new_voo = models.Voo(**voo_data)
    db.add(new_voo)
    db.commit()
    db.refresh(new_voo)
    return schemas.Voo.model_validate(new_voo, from_attributes=True)


@router.get("/", response_model=List[schemas.Voo])
def get_voos(
    origem: Annotated[Optional[str], Query(description="Filter by origin airport")] = None,
    destino: Annotated[Optional[str], Query(description="Filter by destination airport")] = None,
    data_ida: Annotated[Optional[date], Query(description="Filter by departure date")] = None,
    companhia_aerea: Annotated[Optional[str], Query(description="Filter by airline")] = None,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Get all voos with optional filters"""
    query = db.query(models.Voo).filter(models.Voo.deleted_at.is_(None))
    
    if origem:
        query = query.filter(models.Voo.origem.ilike(f"%{origem}%"))
    if destino:
        query = query.filter(models.Voo.destino.ilike(f"%{destino}%"))
    if data_ida:
        query = query.filter(models.Voo.data_ida == data_ida)
    if companhia_aerea:
        query = query.filter(models.Voo.companhia_aerea.ilike(f"%{companhia_aerea}%"))
    
    voos = query.all()
    return [schemas.Voo.model_validate(voo, from_attributes=True) for voo in voos]


@router.get("/{voo_id}", response_model=schemas.VooComReservas)
def get_voo(voo_id: int, db: Annotated[Session, Depends(get_db)]):
    """Get a specific voo by ID"""
    voo = db.query(models.Voo).filter(
        models.Voo.id_voo == voo_id,
        models.Voo.deleted_at.is_(None)
    ).first()
    
    if not voo:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Voo not found"
        )
    return voo


@router.get("/numero/{numero_voo}", response_model=schemas.Voo)
def get_voo_by_numero(
    numero_voo: str, 
    db: Annotated[Session, Depends(get_db)]
):
    """Get a voo by flight number"""
    voo = db.query(models.Voo).filter(
        models.Voo.numero_voo == numero_voo,
        models.Voo.deleted_at.is_(None)
    ).first()
    
    if not voo:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Voo not found with this flight number"
        )
    return schemas.Voo.model_validate(voo, from_attributes=True)


@router.put("/{voo_id}", response_model=schemas.Voo)
def update_voo(
    voo_id: int, 
    voo_update: schemas.VooUpdate, 
    db: Annotated[Session, Depends(get_db)]
):
    """Update a voo"""
    db_voo = db.query(models.Voo).filter(
        models.Voo.id_voo == voo_id,
        models.Voo.deleted_at.is_(None)
    ).first()
    
    if not db_voo:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Voo not found"
        )
    
    update_data = voo_update.model_dump(exclude_unset=True)
    
    # Convert enum to string for database storage
    if "tier" in update_data and update_data["tier"] is not None:
        update_data["tier"] = update_data["tier"].value
    
    for key, value in update_data.items():
        setattr(db_voo, key, value)
    
    db.commit()
    db.refresh(db_voo)
    return schemas.Voo.model_validate(db_voo, from_attributes=True)


@router.delete("/{voo_id}")
def delete_voo(voo_id: int, db: Annotated[Session, Depends(get_db)]):
    """Soft delete a voo"""
    voo = db.query(models.Voo).filter(
        models.Voo.id_voo == voo_id,
        models.Voo.deleted_at.is_(None)
    ).first()
    
    if not voo:
        raise HTTPException(
            status_code=HttpStatusCodes.NOT_FOUND, 
            detail="Voo not found"
        )
    
    # Check if there are active reservations for this flight
    active_reservas = db.query(models.Reserva).filter(
        models.Reserva.id_voo == voo_id,
        models.Reserva.status == models.StatusReserva.ATIVA.value,
        models.Reserva.deleted_at.is_(None)
    ).first()
    
    if active_reservas:
        raise HTTPException(
            status_code=HttpStatusCodes.BAD_REQUEST,
            detail="Cannot delete flight with active reservations"
        )
    
    # Soft delete by setting deleted_at timestamp
    from datetime import datetime, UTC
    voo.deleted_at = datetime.now(UTC)
    db.commit()
    return {"message": "Voo deleted successfully"}