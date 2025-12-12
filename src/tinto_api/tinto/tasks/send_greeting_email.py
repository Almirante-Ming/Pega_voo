from tinto.celery_app import app
from tinto.utils import SessionLocal
from tinto import models


@app.task(name='send_greeting_email')
def send_greeting_email(person_id: int):

    db = SessionLocal()
    
    try:
        person = db.query(models.Person).filter(models.Person.id == person_id).first()
        if not person:
            raise Exception(f"Person with ID {person_id} not found")
        
        email_subject = "Bem-vindo ao Pega Voo"
        email_body = f"""
Prezado(a) {person.full_name},

Bem-vindo ao Pega Voo 

Estamos entusiasmados em tê-lo como novo membro. Sua conta foi criada com sucesso e está pronta para uso.

Agora você pode:
  ✈️ Navegar pelos voos disponíveis
  🎫 Reservar passagens para seus voos desejados

Se tiver dúvidas ou precisar de assistência, entre em contato com nossa equipe de suporte:
Email: support@tinto.com (ficticeo)
Telefone: +55 (67) 98133-5413

Obrigado por nos escolher. Esperamos ajudá-lo a reservar seu próximo voo!

Atenciosamente,
Equipe do Sistema de Reserva Tinto
"""
        
        from tinto.tasks.send_mail import send_email
        
        send_email.delay(person.email, email_subject, email_body)
        
        db.close()
        return {
            'status': 'success',
            'person_id': person_id,
            'email': person.email,
            'message': f'Greeting email sent to {person.email}'
        }
    
    except Exception as e:
        db.close()
        raise Exception(f"Error sending greeting email: {str(e)}")
