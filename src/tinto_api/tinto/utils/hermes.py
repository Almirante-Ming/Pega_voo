import smtplib
from email.mime.text import MIMEText
import os

SENDER = str(os.getenv('SENDER'))
LOCK = str(os.getenv('LOCK'))


def send_mail(reciver, kcode):
    corpo = f"Seu código de verificação é: {kcode}"
    msg = MIMEText(corpo)
    msg['Subject'] = 'Código de Verificação'
    msg['From'] = SENDER
    msg['To'] = reciver

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        try:
            server.starttls()
            server.login(SENDER, LOCK)
            server.send_message(msg)
        except:
            raise ConnectionError
