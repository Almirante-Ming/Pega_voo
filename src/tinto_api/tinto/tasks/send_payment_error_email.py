from tinto.celery_app import app
from tinto.utils import SessionLocal
from tinto import models


@app.task(name='send_payment_error_email')
def send_payment_error_email(ticket_id: int):
    """
    Send payment error email to passenger when payment confirmation fails.
    
    Args:
        ticket_id: The ID of the ticket with failed payment
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
        
        # Prepare error email content
        email_subject = "Payment Confirmation Issue - Action Required"
        email_body = f"""
Dear {passenger.full_name},

We were unable to confirm your payment for the flight ticket within the expected timeframe.

Flight Details:
  - From: {flight.origin_city} ({flight.origin_airport})
  - To: {flight.destination_city} ({flight.destination_airport})
  - Flight Number: {flight.flight_number}
  - Seat: {ticket.seat_number}
  - Departure: {ticket.boarding_time.strftime('%Y-%m-%d %H:%M')}

Ticket ID: {ticket_id}

Your seat has been released back to availability. Please try booking again or contact our support team for assistance.

If you have any questions, please contact our customer service:
Email: support@tinto.com
Phone: +55 (XX) XXXX-XXXX

Thank you,
Tinto Booking System
"""
        
        # Import send_email task
        from tinto.tasks.send_mail import send_email
        
        # Send error email
        send_email.delay(passenger.email, email_subject, email_body)
        
        db.close()
        return {
            'status': 'success',
            'ticket_id': ticket_id,
            'passenger_email': passenger.email,
            'message': f'Error notification email sent to {passenger.email}'
        }
    
    except Exception as e:
        db.close()
        raise Exception(f"Error sending payment error email: {str(e)}")
