import stripe
import os
from tinto.celery_app import app
from tinto.utils import SessionLocal
from tinto import models


STRIPE_SECRET_KEY = str(os.getenv('STRIPE_SECRET_KEY'))
STRIPE_PUBLIC_KEY = str(os.getenv('STRIPE_PUBLIC_KEY'))
FRONT_REDIRECT_URL = str(os.getenv('FRONT_REDIRECT_URL', 'http://localhost:3000'))

stripe.api_key = STRIPE_SECRET_KEY


@app.task(name='checkout')
def create_checkout_session(ticket_id: int, passenger_email: str):
    """
    Create a Stripe checkout session for a ticket reservation
    
    Args:
        ticket_id: The ID of the reserved ticket
        passenger_email: The email of the passenger for the checkout session
    
    Returns:
        dict: Contains status and checkout_url for redirecting to Stripe payment page
    """
    db = SessionLocal()
    
    try:
        # Fetch the ticket from database
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not ticket:
            raise Exception(f"Ticket with ID {ticket_id} not found")
        
        # Fetch flight details for product information
        flight = db.query(models.Flight).filter(models.Flight.id == ticket.flight_id).first()
        if not flight:
            raise Exception(f"Flight with ID {ticket.flight_id} not found")
        
        # Convert price to cents (Stripe expects cents)
        price_cents = int(float(ticket.price) * 100)  #type: ignore
        
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': f'Flight Ticket - {flight.departure_city} to {flight.arrival_city}',
                            'description': f'Seat Class: {ticket.seat_class.value} | Flight: {flight.id} | Ticket ID: {ticket_id}',
                            'metadata': {
                                'ticket_id': str(ticket_id),
                                'flight_id': str(flight.id),
                            }
                        },
                        'unit_amount': price_cents,
                    },
                    'quantity': 1,
                }
            ],
            customer_email=passenger_email,
            mode='payment',
            success_url=f'{FRONT_REDIRECT_URL}/payment/success?ticket_id={ticket_id}',
            cancel_url=f'{FRONT_REDIRECT_URL}/payment/cancel?ticket_id={ticket_id}',
            metadata={
                'ticket_id': str(ticket_id),
                'passenger_id': str(ticket.passenger_id),
            }
        )
        
        db.close()
        
        return {
            'status': 'success',
            'checkout_url': checkout_session.url,
            'session_id': checkout_session.id,
            'ticket_id': ticket_id
        }
    
    except Exception as e:
        db.close()
        raise Exception(f"Error creating checkout session: {str(e)}")
