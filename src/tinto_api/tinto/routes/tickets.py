from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import Annotated, List, Optional
from http import HTTPStatus as HTTPStatus

from tinto import schemas, models
from tinto.utils import DBSession, Seat_Class, require_authenticated_user, require_c_admin_or_sysadmin, get_current_active_user

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=schemas.Ticket, dependencies=[Depends(require_authenticated_user)])
def create_ticket(
    ticket: schemas.TicketCreate, 
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    flight = db.query(models.Flight).filter(models.Flight.id == ticket.flight_id).first()
    if not flight:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Flight not found")
    
    # Determine available seats based on seat class
    if ticket.seat_class == Seat_Class.ECONOMY:
        available = flight.avaliable_seats - flight.premium_seats
    else:
        # All non-economy seats are considered "premium"
        available = flight.premium_seats
    
    # Count already booked seats for this class
    booked_count = db.query(models.Ticket).filter(
        models.Ticket.flight_id == ticket.flight_id,
        models.Ticket.seat_class == ticket.seat_class
    ).count()
    
    if booked_count >= available:  #type: ignore
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"No available {ticket.seat_class.value} seats on this flight")
    
    # Create ticket with current user as passenger and status as "reserved"
    new_ticket = models.Ticket(
        flight_id=ticket.flight_id,
        passenger_id=current_user.id,
        seat_class=ticket.seat_class,
        price=ticket.price,
        status="reserved"
    )
    db.add(new_ticket)
    db.flush()  # Flush to get the ticket ID without committing
    
    # Find an available seat of the same class without a ticket_id
    available_seat = db.query(models.Seat).filter(
        models.Seat.flight_id == ticket.flight_id,
        models.Seat.seat_class == ticket.seat_class.value,
        models.Seat.ticket_id == None  # Only unassigned seats
    ).first()
    
    if not available_seat:
        db.rollback()
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"No available {ticket.seat_class.value} seats on this flight")
    
    # Update the seat with the ticket ID and mark as unavailable
    available_seat.ticket_id = new_ticket.id
    available_seat.is_available = False
    
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.get("/", response_model=List[schemas.Ticket], dependencies=[Depends(require_c_admin_or_sysadmin)])
def get_all_tickets(
    db: DBSession,
    flight_id: Optional[int] = Query(None, description="Filter by flight ID"),
    passenger_id: Optional[int] = Query(None, description="Filter by passenger ID"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    query = db.query(models.Ticket)
    
    if flight_id:
        query = query.filter(models.Ticket.flight_id == flight_id)
    if passenger_id:
        query = query.filter(models.Ticket.passenger_id == passenger_id)
    if status:
        query = query.filter(models.Ticket.status == status)
    
    return query.all()

@router.get("/my-tickets", response_model=List[schemas.Ticket], dependencies=[Depends(require_authenticated_user)])
def get_my_tickets(
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user),
    status: Optional[str] = Query(None, description="Filter by status")
):
    query = db.query(models.Ticket).filter(
        models.Ticket.passenger_id == current_user.id
    )
    
    if status:
        query = query.filter(models.Ticket.status == status)
    
    return query.all()

@router.get("/{ticket_id}", response_model=schemas.Ticket, dependencies=[Depends(require_authenticated_user)])
def get_ticket(
    ticket_id: Annotated[int, Path(title="The ID of the ticket to retrieve")],
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Ticket not found")
    
    if str(current_user.person_type.value) == "customer" and int(current_user.id) != int(ticket.passenger_id): #type:ignore
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You can only access your own tickets")
    
    return ticket

@router.put("/{ticket_id}", response_model=schemas.Ticket, dependencies=[Depends(require_authenticated_user)])
def update_ticket(
    ticket_id: Annotated[int, Path(title="The ID of the ticket to update")],
    ticket_update: schemas.TicketUpdate,
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Ticket not found")
    
    if str(current_user.person_type.value) == "customer" and int(current_user.id) != int(db_ticket.passenger_id):  #type:ignore
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You can only update your own tickets")
    
    update_data = ticket_update.model_dump(exclude_unset=True)
    
    if "flight_id" in update_data:
        flight = db.query(models.Flight).filter(models.Flight.id == update_data["flight_id"]).first()
        if not flight:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Flight not found")
    
    if "passenger_id" in update_data:
        passenger = db.query(models.Person).filter(models.Person.id == update_data["passenger_id"]).first()
        if not passenger:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Passenger not found")
    
    for key, value in update_data.items():
        setattr(db_ticket, key, value)
    
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.delete("/{ticket_id}", dependencies=[Depends(require_authenticated_user)])
def cancel_ticket(
    ticket_id: Annotated[int, Path(title="The ID of the ticket to cancel")],
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Ticket not found")
    
    if str(current_user.person_type.value) == "customer" and int(current_user.id) != int(ticket.passenger_id):  #type:ignore
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You can only cancel your own tickets")
    
    setattr(ticket, 'status', 'indisponível')
    
    db.commit()
    return {"message": "Ticket cancelled"}