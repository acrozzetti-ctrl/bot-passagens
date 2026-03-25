import requests
import time
import smtplib
import os
from email.mime.text import MIMEText

API_KEY = os.getenv("API_KEY")
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

ROTAS = [
    ("GRU", "JFK", "13/12/2026", 3500),
    ("JFK", "MIA", "22/12/2026", 800),
    ("MIA", "GRU", "10/01/2027", 3500)
]

def enviar_email(msg):
    corpo = MIMEText(msg)
    corpo["Subject"] = "🔥 Promoção de Passagem!"
    corpo["From"] = EMAIL_REMETENTE
    corpo["To"] = EMAIL_DESTINO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.send_message(corpo)

def checar_voos():
    for origem, destino, data, limite in ROTAS:
        url = "https://api.tequila.kiwi.com/v2/search"
        
        headers = {"apikey": API_KEY}
        
        params = {
            "fly_from": origem,
            "fly_to": destino,
            "date_from": data,
            "date_to": data,
            "curr": "BRL",
            "limit": 1
        }

        response = requests.get(url, headers=headers, params=params)
        data_json = response.json()

        if not data_json.get("data"):
            continue

        preco = data_json["data"][0]["price"]

        if preco < limite:
            msg = f"PROMOÇÃO! {origem} → {destino} por R$ {preco}"
            enviar_email(msg)

def run():
    while True:
        checar_voos()
        time.sleep(7200)

run()
