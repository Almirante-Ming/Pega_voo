from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import Annotated, List, Optional
from http import HTTPStatus as HTTPStatus

from tinto import schemas, models
from tinto.utils import DBSession, Seat_Class, require_authenticated_user, require_c_admin_or_sysadmin, get_current_active_user
from tinto.tasks import create_checkout_session
from tinto.celery_app import app as celery_app

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=dict, dependencies=[Depends(require_authenticated_user)])
def create_ticket(
    ticket: schemas.TicketCreate, 
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    """
    Create a ticket reservation and initiate Stripe checkout process.
    
    1. Validates flight exists
    2. Checks available seats for the requested class
    3. Reserves a seat and creates ticket with status "reserved"
    4. Sends checkout task to Celery to generate Stripe payment link
    
    Returns:
        dict: Contains ticket info and checkout URL for payment
    """
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
    
    # Find an available seat of the same class without a ticket_id
    available_seat = db.query(models.Seat).filter(
        models.Seat.flight_id == ticket.flight_id,
        models.Seat.seat_class == ticket.seat_class.value,
        models.Seat.ticket_id == None  # Only unassigned seats
    ).first()
    
    if not available_seat:
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
    
    # Update the seat with the ticket ID
    available_seat.ticket_id = new_ticket.id
    
    db.commit()
    db.refresh(new_ticket)
    
    # Send to Celery task to create Stripe checkout session
    # This will generate payment link and return it to the client
    checkout_task = create_checkout_session.delay(new_ticket.id, current_user.email)
    
    return {
        "ticket_id": new_ticket.id,
        "flight_id": new_ticket.flight_id,
        "seat_class": new_ticket.seat_class.value,
        "price": str(new_ticket.price),
        "status": new_ticket.status,
        "created_at": new_ticket.created_at.isoformat(),
        "task_id": checkout_task.id,
        "message": "Ticket reserved. Redirect to checkout URL on frontend after receiving checkout task result"
    }

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

@router.get("/checkout/{task_id}", dependencies=[Depends(require_authenticated_user)])
def get_checkout_result(
    task_id: Annotated[str, Path(title="The Celery task ID for the checkout session")],
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    """
    Get the result of a checkout session creation task.
    Returns the Stripe payment URL when the task is complete.
    
    Args:
        task_id: The Celery task ID returned from ticket creation
    
    Returns:
        dict: Contains checkout_url (Stripe payment link) and other session info
    """
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        if task_result.state == 'PENDING':
            return {
                "status": "pending",
                "message": "Checkout session is being created. Please wait.",
                "task_id": task_id
            }
        elif task_result.state == 'SUCCESS':
            result = task_result.result
            return {
                "status": "success",
                "checkout_url": result.get('checkout_url'),
                "session_id": result.get('session_id'),
                "ticket_id": result.get('ticket_id'),
                "message": "Checkout session created. Redirect user to checkout_url"
            }
        elif task_result.state == 'FAILURE':
            return {
                "status": "failed",
                "message": f"Checkout session creation failed: {str(task_result.result)}",
                "task_id": task_id
            }
        else:
            return {
                "status": task_result.state.lower(),
                "message": f"Checkout session status: {task_result.state}",
                "task_id": task_id
            }
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving checkout status: {str(e)}"
        )

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