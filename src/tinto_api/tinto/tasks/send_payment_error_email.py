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
        
        email_subject = "Problema na Confirmação de Pagamento - Ação Necessária"
        email_body = f"""
Prezado(a) {passenger.full_name},

Não conseguimos confirmar seu pagamento prazo esperado.

Detalhes do Voo:
  - De: {flight.origin_city} ({flight.origin_airport})
  - Para: {flight.destination_city} ({flight.destination_airport})
  - Número do Voo: {flight.flight_number}
  - Assento: {ticket.seat_number}
  - Partida: {ticket.boarding_time.strftime('%d/%m/%Y às %H:%M')}

ID da Passagem: {ticket_id}

Por favor, tente reservar novamente ou entre em contato com nossa equipe de suporte para assistência.

Se tiver dúvidas, por favor entre em contato com nosso atendimento ao cliente:
Email: support@tinto.com
Telefone: +55 (67) 98133-5413

Obrigado,
Pega Voo
"""
        
        from tinto.tasks.send_mail import send_email
        
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
