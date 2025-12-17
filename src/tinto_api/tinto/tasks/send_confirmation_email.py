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
        ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not ticket:
            raise Exception(f"Ticket with ID {ticket_id} not found")
        
        passenger = db.query(models.Person).filter(
            models.Person.id == ticket.passenger_id
        ).first()
        
        if not passenger:
            raise Exception(f"Passenger with ID {ticket.passenger_id} not found")
        
        flight = db.query(models.Flight).filter(
            models.Flight.id == ticket.flight_id
        ).first()
        
        if not flight:
            raise Exception(f"Flight with ID {ticket.flight_id} not found")
        
        email_subject = "Pagamento Confirmado - Reserva de Voo"
        email_body = f"""
Prezado(a) {passenger.full_name},

Seu pagamento foi confirmado com sucesso!

Detalhes do Voo:
  - De: {flight.origin_city} ({flight.origin_airport})
  - Para: {flight.destination_city} ({flight.destination_airport})
  - Número do Voo: {flight.flight_number}
  - Assento: {ticket.seat_number}
  - Classe do Assento: {ticket.seat_class.value.upper()}
  - Preço: R$ {ticket.price:.2f}
  - Partida: {ticket.boarding_time.strftime('%d/%m/%Y às %H:%M')}
  - Chegada: {ticket.arrival_time.strftime('%d/%m/%Y às %H:%M')}

Sua passagem agora está confirmada e pronta para check-in. Guarde este email de confirmação para seus registros.

Importante: Chegue ao aeroporto com pelo menos 2 horas de antecedência à partida.

Obrigado por reservar conosco!

Atenciosamente,
Pega Voo
"""
        
        from tinto.tasks.send_mail import send_email
        
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
