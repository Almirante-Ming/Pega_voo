import stripe
import os
from tinto.celery_app import app
from tinto.utils import SessionLocal
from tinto import models


STRIPE_SECRET_KEY = str(os.getenv('STRIPE_SECRET_KEY'))
stripe.api_key = STRIPE_SECRET_KEY

MAX_PAYMENT_CHECK_TRIES = 20
PAYMENT_CHECK_DELAY = 10  # seconds


def release_seat(ticket_id: int):
    """
    Release a seat back to available status when payment fails.
    
    Args:
        ticket_id: The ID of the ticket
    """
    db = SessionLocal()
    try:
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not ticket:
            return
        
        seat = db.query(models.Seat).filter(
            models.Seat.flight_id == ticket.flight_id,
            models.Seat.seat_number == ticket.seat_number
        ).first()
        
        if seat:
            setattr(seat, 'is_available', True)
            setattr(seat, 'ticket_id', None)
        
        setattr(ticket, 'status', 'cancelled')
        db.commit()
    finally:
        db.close()


def await_payment_confirmation(session_id: str, ticket_id: int, max_tries: int = MAX_PAYMENT_CHECK_TRIES):
    """
    Poll Stripe to check if payment was completed.
    
    Args:
        session_id: The Stripe checkout session ID
        ticket_id: The ID of the ticket
        max_tries: Maximum number of attempts to check payment
    
    Returns:
        dict: Payment status and result
    """
    import time
    
    for attempt in range(1, max_tries + 1):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == "paid":
                return {
                    'status': 'confirmed',
                    'session': session,
                    'attempts': attempt
                }
            
            if attempt < max_tries:
                time.sleep(PAYMENT_CHECK_DELAY)
        
        except Exception as e:
            if attempt < max_tries:
                time.sleep(PAYMENT_CHECK_DELAY)
            else:
                return {
                    'status': 'error',
                    'attempts': attempt,
                    'message': str(e)
                }
    
    return {
        'status': 'failed',
        'attempts': max_tries,
        'message': 'Payment confirmation timeout'
    }


@app.task(name='check_payment_confirmation')
def check_payment_confirmation(session_id: str, ticket_id: int, passenger_email: str):
    """
    Poll Stripe to check if payment was confirmed and update ticket status accordingly.
    
    Args:
        session_id: The Stripe checkout session ID
        ticket_id: The ID of the ticket
        passenger_email: The passenger's email for error notification
    """
    db = SessionLocal()
    
    try:
        payment_result = await_payment_confirmation(session_id, ticket_id)
        
        if payment_result['status'] == 'confirmed':
            ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
            if ticket:
                setattr(ticket, 'status', 'marked')
                
                seat = db.query(models.Seat).filter(
                    models.Seat.flight_id == ticket.flight_id,
                    models.Seat.seat_number == ticket.seat_number
                ).first()
                
                if seat:
                    setattr(seat, 'is_available', False)
                
                db.commit()
            
            db.close()
            
            from tinto.tasks.send_confirmation_email import send_confirmation_email
            send_confirmation_email.delay(ticket_id)
            
            return {
                'status': 'success',
                'message': f'Payment confirmed after {payment_result["attempts"]} checks',
                'ticket_id': ticket_id
            }
        else:
            db.close()
            
            release_seat(ticket_id)
            from tinto.tasks.send_payment_error_email import send_payment_error_email
            send_payment_error_email.delay(ticket_id)
            
            return {
                'status': 'failed',
                'message': payment_result.get('message', 'Payment confirmation failed'),
                'attempts': payment_result.get('attempts'),
                'ticket_id': ticket_id
            }
    except Exception as e:
        db.close()
        raise Exception(f"Error checking payment confirmation: {str(e)}")
