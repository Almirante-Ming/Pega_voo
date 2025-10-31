from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import and_, or_
from typing import Annotated, List, Optional
from http import HTTPStatus as HTTPStatus
from datetime import datetime

from tinto import schemas, models
from tinto.utils import DBSession, Flight_Status, require_c_admin_or_sysadmin, require_authenticated_user

router = APIRouter(prefix="/flights", tags=["Flights"])

# Admin routes (require admin permissions)
admin_router = APIRouter(dependencies=[Depends(require_c_admin_or_sysadmin)])

@admin_router.post("/", response_model=schemas.Flight)
def create_flight(flight: schemas.FlightCreate, db: DBSession):
    # Check if airline exists
    airline = db.query(models.Airline).filter(models.Airline.id == flight.airline_id).first()
    if not airline:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Airline not found")
    
    # Check if flight number already exists
    existing_flight = db.query(models.Flight).filter(models.Flight.flight_number == flight.flight_number).first()
    if existing_flight:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Flight number already exists")
    
    new_flight = models.Flight(**flight.model_dump())
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)
    return new_flight

@admin_router.put("/{flight_id}", response_model=schemas.Flight)
def update_flight(
    flight_id: Annotated[int, Path(title="The ID of the flight to update")],
    flight_update: schemas.FlightUpdate,
    db: DBSession
):
    db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    if not db_flight:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flight not found")
    
    update_data = flight_update.model_dump(exclude_unset=True)
    
    # Check if airline exists if airline_id is being updated
    if "airline_id" in update_data:
        airline = db.query(models.Airline).filter(models.Airline.id == update_data["airline_id"]).first()
        if not airline:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Airline not found")
    
    # Check for flight number conflicts if it's being updated
    if "flight_number" in update_data and update_data["flight_number"] != db_flight.flight_number:
        existing_flight = db.query(models.Flight).filter(
            models.Flight.flight_number == update_data["flight_number"],
            models.Flight.id != flight_id
        ).first()
        if existing_flight:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Flight number already exists")
    
    for key, value in update_data.items():
        setattr(db_flight, key, value)
    
    db.commit()
    db.refresh(db_flight)
    return db_flight

@admin_router.delete("/{flight_id}")
def delete_flight(
    flight_id: Annotated[int, Path(title="The ID of the flight to delete")],
    db: DBSession
):
    flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flight not found")
    
    # Mark as cancelled instead of hard delete
    setattr(flight, 'status', Flight_Status.CANCELLED)
    db.commit()
    return {"message": "Flight cancelled"}

# Public routes (require authentication but accessible to customers)
@router.get("/", response_model=List[schemas.Flight], dependencies=[Depends(require_authenticated_user)])
def get_flights(
    db: DBSession,
    origin_city: Optional[str] = Query(None, description="Filter by origin city"),
    destination_city: Optional[str] = Query(None, description="Filter by destination city"),
    departure_date: Optional[str] = Query(None, description="Filter by departure date (YYYY-MM-DD)"),
    airline_id: Optional[int] = Query(None, description="Filter by airline ID")
):
    query = db.query(models.Flight).filter(models.Flight.status == Flight_Status.SCHEDULED)
    
    if origin_city:
        query = query.filter(models.Flight.origin_city.ilike(f"%{origin_city}%"))
    if destination_city:
        query = query.filter(models.Flight.destination_city.ilike(f"%{destination_city}%"))
    if departure_date:
        try:
            date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()
            query = query.filter(models.Flight.departure_time.date() == date_obj)
        except ValueError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid date format. Use YYYY-MM-DD")
    if airline_id:
        query = query.filter(models.Flight.airline_id == airline_id)
    
    return query.all()

@router.get("/{flight_id}", response_model=schemas.Flight, dependencies=[Depends(require_authenticated_user)])
def get_flight(
    flight_id: Annotated[int, Path(title="The ID of the flight to retrieve")],
    db: DBSession
):
    flight = db.query(models.Flight).filter(
        models.Flight.id == flight_id,
        models.Flight.status == Flight_Status.SCHEDULED
    ).first()
    if not flight:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flight not found")
    return flight

# Include admin routes
router.include_router(admin_router)