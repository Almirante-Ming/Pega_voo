from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import func
from typing import Annotated, List, Optional, cast, Dict
from http import HTTPStatus
from datetime import datetime

from tinto import schemas, models
from tinto.utils import DBSession, Flight_Status, Seat_Class, require_c_admin_or_sysadmin, require_authenticated_user

router = APIRouter(prefix="/flights", tags=["Flights"])

admin_router = APIRouter(dependencies=[Depends(require_c_admin_or_sysadmin)])

def build_flight_with_seats_and_prices(flight: models.Flight, db: DBSession) -> Dict:
    """Build flight response with prices by class"""
    tickets_dict = {}
    if flight.seats:
        seats_by_class = {}
        for seat in flight.seats:
            class_name = seat.seat_class.value if hasattr(seat.seat_class, 'value') else str(seat.seat_class)
            if class_name not in seats_by_class:
                seats_by_class[class_name] = seat
        
        for class_name, seat in seats_by_class.items():
            if seat.price is not None:
                tickets_dict[class_name] = float(str(seat.price))
    
    flight_dict = flight.__dict__.copy()
    airline_name = flight.airline.name if flight.airline else "Unknown"
    flight_dict['airline_name'] = airline_name
    flight_dict['tickets'] = tickets_dict
    
    return flight_dict


@admin_router.post("/", response_model=schemas.Flight)
def create_flight(flight: schemas.FlightCreateRequest, db: DBSession):
    airline = db.query(models.Airline).filter(models.Airline.id == flight.airline_id).first()
    if not airline:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Airline not found")
    
    existing_flight = db.query(models.Flight).filter(models.Flight.flight_number == flight.flight_number).first()
    if existing_flight:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Flight number already exists")
    
    premium_seats = cast(int, flight.premium_seats)
    if premium_seats > 0 and flight.premium_price is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="premium_price is required when premium_seats > 0")
    
    total_seats = cast(int, flight.avaliable_seats)
    economy_seats = total_seats - premium_seats
    
    flight_data = flight.model_dump(exclude={'economy_price', 'premium_price'})
    flight_data['economy_seats'] = economy_seats
    flight_data['status'] = Flight_Status.SCHEDULED
    new_flight = models.Flight(**flight_data)
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)
    db.refresh(new_flight, ['airline'])
    
    seat_columns = ['A', 'B', 'C', 'D', 'E', 'F']
    total_seats = cast(int, new_flight.avaliable_seats)
    
    seats_per_row = len(seat_columns)
    num_rows = (total_seats + seats_per_row - 1) // seats_per_row 
    
    seat_count = 1
    for row in range(1, num_rows + 1):
        for col in seat_columns:
            if seat_count > total_seats:
                break
                
            seat_number = f"{row}{col}"
            
            if seat_count <= premium_seats:
                seat_class = Seat_Class.PREMIUM.value
                seat_price = flight.premium_price
            else:
                seat_class = Seat_Class.ECONOMY.value
                seat_price = flight.economy_price
            
            new_seat = models.Seat(
                flight_id=new_flight.id,
                seat_number=seat_number,
                seat_class=seat_class,
                price=seat_price,
                is_available=True
            )
            db.add(new_seat)
            seat_count += 1
        
        if seat_count > total_seats:
            break
    
    db.commit()
    db.refresh(new_flight, ['airline'])
    flight_dict = new_flight.__dict__.copy()
    flight_dict['airline_name'] = new_flight.airline.name if new_flight.airline else "Unknown"
    return flight_dict

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
    
    if "airline_id" in update_data:
        airline = db.query(models.Airline).filter(models.Airline.id == update_data["airline_id"]).first()
        if not airline:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Airline not found")
    
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
    db.refresh(db_flight, ['airline'])
    flight_dict = db_flight.__dict__.copy()
    flight_dict['airline_name'] = db_flight.airline.name if db_flight.airline else "Unknown"
    return flight_dict

@admin_router.delete("/{flight_id}")
def delete_flight(
    flight_id: Annotated[int, Path(title="The ID of the flight to delete")],
    db: DBSession
):
    flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flight not found")
    
    setattr(flight, 'status', Flight_Status.CANCELLED)
    db.commit()
    return {"message": "Flight cancelled"}

@router.get("/", response_model=List[schemas.FlightWithSeatsAndPrices], dependencies=[Depends(require_authenticated_user)])
def get_flights(
    db: DBSession,
    origin_city: Optional[str] = Query(None, description="Filter by origin city"),
    destination_city: Optional[str] = Query(None, description="Filter by destination city"),
    departure_date: Optional[str] = Query(None, description="Filter by departure date (YYYY-MM-DD)"),
    stops_count: Optional[int] = Query(None, description="Filter by number of stops")
):
    query = db.query(models.Flight).filter(models.Flight.status == Flight_Status.SCHEDULED)
    
    if origin_city and origin_city.strip():
        search_term = origin_city.strip().lower()
        query = query.filter(
            func.unaccent(func.lower(models.Flight.origin_city)).contains(
                func.unaccent(search_term)
            )
        )
    
    if destination_city and destination_city.strip():
        search_term = destination_city.strip().lower()
        query = query.filter(
            func.unaccent(func.lower(models.Flight.destination_city)).contains(
                func.unaccent(search_term)
            )
        )
    
    if departure_date and departure_date.strip():
        try:
            date_obj = datetime.strptime(departure_date.strip(), "%Y-%m-%d").date()
            query = query.filter(func.date(models.Flight.departure_time) == date_obj)
        except ValueError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid date format. Use YYYY-MM-DD")
    
    if stops_count is not None:
        query = query.filter(models.Flight.stops_count == stops_count)
    
    flights = query.all()
    return [build_flight_with_seats_and_prices(flight, db) for flight in flights]

@router.get("/{flight_id}", response_model=schemas.FlightWithSeatsAndPrices, dependencies=[Depends(require_authenticated_user)])
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
    return build_flight_with_seats_and_prices(flight, db)

@router.get("/{flight_id}/seats", response_model=List[schemas.Seat], dependencies=[Depends(require_authenticated_user)])
def get_flight_seats_by_id(
    flight_id: Annotated[int, Path(title="The ID of the flight")],
    db: DBSession
):
    """Get all seats for a flight by flight ID"""
    flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flight not found")
    
    seats = db.query(models.Seat).filter(models.Seat.flight_id == flight_id).all()
    return seats

@router.get("/seats/by-number/{flight_number}", response_model=List[schemas.Seat], dependencies=[Depends(require_authenticated_user)])
def get_flight_seats_by_number(
    flight_number: Annotated[str, Path(title="The flight number")],
    db: DBSession
):
    """Get all seats for a flight by flight number. Available for all authenticated users."""
    flight = db.query(models.Flight).filter(models.Flight.flight_number == flight_number).first()
    if not flight:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Flight not found")
    
    seats = db.query(models.Seat).filter(models.Seat.flight_id == flight.id).all()
    return seats

router.include_router(admin_router)