from tinto.celery_app import app
from email.mime.text import MIMEText
import smtplib
import os

SENDER = str(os.getenv('SENDER'))
LOCK = str(os.getenv('LOCK'))

@app.task(name='send_email')
def send_email(receiver: str, subject: str, body: str):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = receiver

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER, LOCK)
            server.send_message(msg)
        return {"status": "success", "receiver": receiver}
    except Exception as e:
        raise Exception(f"Failed to send email to {receiver}: {str(e)}")