from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import and_
from typing import Annotated, List, Optional
from http import HTTPStatus as HttpStatusCodes
import json

from tinto import schemas, models
from tinto.utils import DBSession, Booking_Status, require_authenticated_user, require_c_admin_or_sysadmin, get_current_active_user

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=schemas.Ticket, dependencies=[Depends(require_authenticated_user)])
def create_ticket(
    ticket: schemas.TicketCreate, 
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    
    purchase_history = db.query(models.PurchaseHistory).filter(models.PurchaseHistory.id == ticket.purchase_history_id).first()
    if not purchase_history:
        raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Purchase history not found")
    
    if str(current_user.p_type.value) == "customer" and int(current_user.id) != int(purchase_history.user_id): #type:ignore
        raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="You can only create tickets for your own purchases")
    
    flight = db.query(models.Flight).filter(models.Flight.id == ticket.flight_id).first()
    if not flight:
        raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Flight not found")
    
    available_seats = int(flight.a_seats)  #type:ignore
    if available_seats <= 0:
        raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="No available seats on this flight")
    
    new_ticket = models.Ticket(**ticket.model_dump())
    db.add(new_ticket)
    

    setattr(flight, 'a_seats', available_seats - 1)
    
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.post("/with-passenger-list", response_model=schemas.Ticket, dependencies=[Depends(require_authenticated_user)])
def create_ticket_with_passenger_list(
    ticket: schemas.TicketCreateWithPassengerList, 
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    ticket_data = ticket.model_dump()
    ticket_data["passengers"] = json.dumps(ticket.passengers)
    
    purchase_history = db.query(models.PurchaseHistory).filter(models.PurchaseHistory.id == ticket.purchase_history_id).first()
    if not purchase_history:
        raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Purchase history not found")
    
    if str(current_user.p_type.value) == "customer" and int(current_user.id) != int(purchase_history.user_id):  #type:ignore
        raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="You can only create tickets for your own purchases")

    flight = db.query(models.Flight).filter(models.Flight.id == ticket.flight_id).first()
    if not flight:
        raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Flight not found")
    
    available_seats = int(flight.a_seats)  #type:ignore
    if available_seats <= 0:
        raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="No available seats on this flight")
    
    new_ticket = models.Ticket(**ticket_data)
    db.add(new_ticket)
    
    setattr(flight, 'a_seats', available_seats - 1)
    
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.get("/", response_model=List[schemas.Ticket], dependencies=[Depends(require_c_admin_or_sysadmin)])
def get_all_tickets(
    db: DBSession,
    purchase_history_id: Optional[int] = Query(None, description="Filter by purchase history ID"),
    flight_id: Optional[int] = Query(None, description="Filter by flight ID"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    query = db.query(models.Ticket)
    
    if purchase_history_id:
        query = query.filter(models.Ticket.purchase_history_id == purchase_history_id)
    if flight_id:
        query = query.filter(models.Ticket.flight_id == flight_id)
    if status:
        try:
            status_enum = Booking_Status(status.lower())
            query = query.filter(models.Ticket.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Invalid status")
    
    return query.all()

@router.get("/my-tickets", response_model=List[schemas.TicketWithParsedPassengers], dependencies=[Depends(require_authenticated_user)])
def get_my_tickets(
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user),
    status: Optional[str] = Query(None, description="Filter by status")
):
    query = db.query(models.Ticket).join(models.PurchaseHistory).filter(
        models.PurchaseHistory.user_id == current_user.id
    )
    
    if status:
        try:
            status_enum = Booking_Status(status.lower())
            query = query.filter(models.Ticket.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Invalid status")
    
    tickets = query.all()
    
    # Convert to TicketWithParsedPassengers format
    result = []
    for ticket in tickets:
        passengers_json = getattr(ticket, 'passengers')
        ticket_dict = {
            "id": ticket.id,
            "purchase_history_id": ticket.purchase_history_id,
            "flight_id": ticket.flight_id,
            "passengers": json.loads(passengers_json),
            "valor": ticket.valor,
            "horario_embarque": ticket.horario_embarque,
            "horario_desembarque": ticket.horario_desembarque,
            "status": ticket.status,
            "dt_create": ticket.dt_create,
            "dt_update": ticket.dt_update
        }
        result.append(schemas.TicketWithParsedPassengers(**ticket_dict))
    
    return result

@router.get("/{ticket_id}", response_model=schemas.TicketWithParsedPassengers, dependencies=[Depends(require_authenticated_user)])
def get_ticket(
    ticket_id: Annotated[int, Path(title="The ID of the ticket to retrieve")],
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=HttpStatusCodes.NOT_FOUND, detail="Ticket not found")
    
    if str(current_user.p_type.value) == "customer":
        purchase_history = db.query(models.PurchaseHistory).filter(models.PurchaseHistory.id == ticket.purchase_history_id).first()
        if not purchase_history or int(current_user.id) != int(purchase_history.user_id): #type:ignore
            raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="You can only access your own tickets")
    
    passengers_json = getattr(ticket, 'passengers')
    ticket_dict = {
        "id": ticket.id,
        "purchase_history_id": ticket.purchase_history_id,
        "flight_id": ticket.flight_id,
        "passengers": json.loads(passengers_json),
        "valor": ticket.valor,
        "horario_embarque": ticket.horario_embarque,
        "horario_desembarque": ticket.horario_desembarque,
        "status": ticket.status,
        "dt_create": ticket.dt_create,
        "dt_update": ticket.dt_update
    }
    
    return schemas.TicketWithParsedPassengers(**ticket_dict)

@router.put("/{ticket_id}", response_model=schemas.Ticket, dependencies=[Depends(require_authenticated_user)])
def update_ticket(
    ticket_id: Annotated[int, Path(title="The ID of the ticket to update")],
    ticket_update: schemas.TicketUpdate,
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=HttpStatusCodes.NOT_FOUND, detail="Ticket not found")
    
    if str(current_user.p_type.value) == "customer":
        purchase_history = db.query(models.PurchaseHistory).filter(models.PurchaseHistory.id == db_ticket.purchase_history_id).first()
        if not purchase_history or int(current_user.id) != int(purchase_history.user_id):  #type:ignore
            raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="You can only update your own tickets")
    
    update_data = ticket_update.model_dump(exclude_unset=True)
    
    if "purchase_history_id" in update_data:
        purchase_history = db.query(models.PurchaseHistory).filter(models.PurchaseHistory.id == update_data["purchase_history_id"]).first()
        if not purchase_history:
            raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Purchase history not found")
        
        if str(current_user.p_type.value) == "customer" and int(current_user.id) != int(purchase_history.user_id):  #type:ignore
            raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="You can only link tickets to your own purchases")
    
    if "flight_id" in update_data:
        flight = db.query(models.Flight).filter(models.Flight.id == update_data["flight_id"]).first()
        if not flight:
            raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Flight not found")
    
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
        raise HTTPException(status_code=HttpStatusCodes.NOT_FOUND, detail="Ticket not found")
    
    if str(current_user.p_type.value) == "customer":
        purchase_history = db.query(models.PurchaseHistory).filter(models.PurchaseHistory.id == ticket.purchase_history_id).first()
        if not purchase_history or int(current_user.id) != int(purchase_history.user_id):  #type:ignore
            raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="You can only cancel your own tickets")
    
    setattr(ticket, 'status', Booking_Status.CANCELLED)
    
    flight = db.query(models.Flight).filter(models.Flight.id == ticket.flight_id).first()
    if flight:
        current_seats = int(flight.a_seats)  #type:ignore
        setattr(flight, 'a_seats', current_seats + 1)
    
    db.commit()
    return {"message": "Ticket cancelled"}