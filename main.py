import smtplib
import time
from email.mime.text import MIMEText

EMAIL_REMETENTE = "acrozzetti@gmail.com"
EMAIL_SENHA = "409575"
EMAIL_DESTINO = "acrozzetti@gmail.com"

def enviar_email(msg):
    corpo = MIMEText(msg)
    corpo["Subject"] = "🔔 Monitor de Passagens"
    corpo["From"] = EMAIL_REMETENTE
    corpo["To"] = EMAIL_DESTINO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.send_message(corpo)

def checar():
    # SIMULA ALERTA (depois melhoramos)
    enviar_email("Seu bot está funcionando! ✈️")

def run():
    while True:
        checar()
        time.sleep(7200)

run()
