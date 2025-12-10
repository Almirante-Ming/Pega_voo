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
    # Build tickets dictionary: {"economy": 100.50, "premium": 250.00}
    tickets_dict = {}
    if flight.seats:
        # Group seats by class and get the price from first seat of each class
        seats_by_class = {}
        for seat in flight.seats:
            class_name = seat.seat_class.value if hasattr(seat.seat_class, 'value') else str(seat.seat_class)
            if class_name not in seats_by_class:
                seats_by_class[class_name] = seat
        
        # Get prices from seats
        for class_name, seat in seats_by_class.items():
            # Handle seats with prices (including 0)
            if seat.price is not None:
                tickets_dict[class_name] = float(str(seat.price))
    
    # Build flight data with airline name
    flight_dict = flight.__dict__.copy()
    # Get airline name
    airline_name = flight.airline.name if flight.airline else "Unknown"
    flight_dict['airline_name'] = airline_name
    flight_dict['tickets'] = tickets_dict
    
    return flight_dict


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
    
    # Validate premium price if premium seats exist
    premium_seats = cast(int, flight.premium_seats)
    if premium_seats > 0 and flight.premium_price is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="premium_price is required when premium_seats > 0")
    
    # Create flight without economy_price and premium_price (they're not part of Flight model)
    flight_data = flight.model_dump(exclude={'economy_price', 'premium_price'})
    new_flight = models.Flight(**flight_data)
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)
    
    # Create seats for the flight (A-I columns, multiple rows)
    seat_columns = ['A', 'B', 'C', 'D', 'E', 'F']
    total_seats = cast(int, new_flight.avaliable_seats)
    
    # Calculate number of rows needed (9 seats per row: A-I)
    seats_per_row = len(seat_columns)
    num_rows = (total_seats + seats_per_row - 1) // seats_per_row 
    
    seat_count = 1
    for row in range(1, num_rows + 1):
        for col in seat_columns:
            if seat_count > total_seats:
                break
                
            seat_number = f"{row}{col}"
            
            # Determine seat class and price: first premium_seats are "premium", rest are "economy"
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
@router.get("/", response_model=List[schemas.FlightWithSeatsAndPrices], dependencies=[Depends(require_authenticated_user)])
def get_flights(
    db: DBSession,
    origin_city: Optional[str] = Query(None, description="Filter by origin city"),
    destination_city: Optional[str] = Query(None, description="Filter by destination city"),
    departure_date: Optional[str] = Query(None, description="Filter by departure date (YYYY-MM-DD)"),
    stops_count: Optional[int] = Query(None, description="Filter by number of stops")
):
    query = db.query(models.Flight).filter(models.Flight.status == Flight_Status.SCHEDULED)
    
    # Filter by origin city (case-insensitive, accent-insensitive partial match)
    if origin_city and origin_city.strip():
        search_term = origin_city.strip().lower()
        query = query.filter(
            func.unaccent(func.lower(models.Flight.origin_city)).contains(
                func.unaccent(search_term)
            )
        )
    
    # Filter by destination city (case-insensitive, accent-insensitive partial match)
    if destination_city and destination_city.strip():
        search_term = destination_city.strip().lower()
        query = query.filter(
            func.unaccent(func.lower(models.Flight.destination_city)).contains(
                func.unaccent(search_term)
            )
        )
    
    # Filter by departure date
    if departure_date and departure_date.strip():
        try:
            date_obj = datetime.strptime(departure_date.strip(), "%Y-%m-%d").date()
            query = query.filter(func.date(models.Flight.departure_time) == date_obj)
        except ValueError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Filter by number of stops
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