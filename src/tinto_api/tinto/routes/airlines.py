from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import or_
from typing import Annotated, List
from http import HTTPStatus as HTTPStatus

from tinto import schemas, models
from tinto.utils import DBSession, User_Status, require_c_admin_or_sysadmin

router = APIRouter(prefix="/airlines", tags=["Airlines"], dependencies=[Depends(require_c_admin_or_sysadmin)])

@router.post("/", response_model=schemas.Airline)
def create_airline(airline: schemas.AirlineCreate, db: DBSession):
    db_airline_check = db.query(models.Airline).filter(
        or_(
            models.Airline.name == airline.name,
            models.Airline.code == airline.code
        )
    ).first()
    if db_airline_check:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Airline name or code already exists.")
    
    new_airline = models.Airline(**airline.model_dump())
    db.add(new_airline)
    db.commit()
    db.refresh(new_airline)
    return new_airline

@router.get("/", response_model=List[schemas.Airline])
def get_airlines(db: DBSession):
    return db.query(models.Airline).filter(models.Airline.status != User_Status.DELETED).all()

@router.get("/{airline_id}", response_model=schemas.Airline)
def get_airline(
    airline_id: Annotated[int, Path(title="The ID of the airline to retrieve")],
    db: DBSession
):
    airline = db.query(models.Airline).filter(
        models.Airline.id == airline_id,
        models.Airline.status != User_Status.DELETED
    ).first()
    if not airline:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Airline not found")
    return airline

@router.put("/{airline_id}", response_model=schemas.Airline)
def update_airline(
    airline_id: Annotated[int, Path(title="The ID of the airline to update")],
    airline_update: schemas.AirlineUpdate,
    db: DBSession
):
    db_airline = db.query(models.Airline).filter(
        models.Airline.id == airline_id,
        models.Airline.status != User_Status.DELETED
    ).first()
    if not db_airline:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Airline not found")
    
    update_data = airline_update.model_dump(exclude_unset=True)
    
    if "name" in update_data and update_data["name"] != db_airline.name:
        existing_name_check = db.query(models.Airline).filter(
            models.Airline.name == update_data["name"],
            models.Airline.id != airline_id
        ).first()
        if existing_name_check:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Airline name already exists")
    
    if "code" in update_data and update_data["code"] != db_airline.code:
        existing_code_check = db.query(models.Airline).filter(
            models.Airline.code == update_data["code"],
            models.Airline.id != airline_id
        ).first()
        if existing_code_check:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Airline code already exists")
    
    for key, value in update_data.items():
        setattr(db_airline, key, value)
    
    db.commit()
    db.refresh(db_airline)
    return db_airline

@router.delete("/{airline_id}")
def delete_airline(
    airline_id: Annotated[int, Path(title="The ID of the airline to delete")],
    db: DBSession
):
    airline = db.query(models.Airline).filter(
        models.Airline.id == airline_id,
        models.Airline.status != User_Status.DELETED
    ).first()
    if not airline:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Airline not found")
    
    setattr(airline, 'status', User_Status.DELETED)
    db.commit()
    return {"message": "Airline marked as deleted"}