from tinto.celery_app import app
from tinto.utils import SessionLocal
from tinto import models


@app.task(name='send_confirmation_email')
def send_confirmation_email(ticket_id: int):
    """
    Send ticket confirmation email to passenger after successful payment.
    
    Args:
        ticket_id: The ID of the confirmed ticket
    """
    db = SessionLocal()
    
    try:
        # Fetch ticket with all related data
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not ticket:
            raise Exception(f"Ticket with ID {ticket_id} not found")
        
        # Fetch passenger details
        passenger = db.query(models.Person).filter(
            models.Person.id == ticket.passenger_id
        ).first()
        
        if not passenger:
            raise Exception(f"Passenger with ID {ticket.passenger_id} not found")
        
        # Fetch flight details
        flight = db.query(models.Flight).filter(
            models.Flight.id == ticket.flight_id
        ).first()
        
        if not flight:
            raise Exception(f"Flight with ID {ticket.flight_id} not found")
        
        # Prepare email content
        email_subject = "Ticket Payment Confirmed - Flight Booking"
        email_body = f"""
Dear {passenger.full_name},

Your flight ticket payment has been successfully confirmed!

Flight Details:
  - From: {flight.origin_city} ({flight.origin_airport})
  - To: {flight.destination_city} ({flight.destination_airport})
  - Flight Number: {flight.flight_number}
  - Seat: {ticket.seat_number}
  - Seat Class: {ticket.seat_class.value.upper()}
  - Price: R$ {ticket.price:.2f}
  - Departure: {ticket.boarding_time.strftime('%Y-%m-%d %H:%M')}
  - Arrival: {ticket.arrival_time.strftime('%Y-%m-%d %H:%M')}

Your ticket is now confirmed and ready for check-in. Please keep this confirmation email for your records.

Important: Arrive at the airport at least 2 hours before departure.

Thank you for booking with us!

Best regards,
Tinto Booking System
"""
        
        # Import send_email task
        from tinto.tasks.send_mail import send_email
        
        # Send email
        send_email.delay(passenger.email, email_subject, email_body)
        
        db.close()
        return {
            'status': 'success',
            'ticket_id': ticket_id,
            'passenger_email': passenger.email,
            'message': f'Confirmation email sent to {passenger.email}'
        }
    
    except Exception as e:
        db.close()
        raise Exception(f"Error sending confirmation email: {str(e)}")
