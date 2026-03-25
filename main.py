import requests

ROTAS = [
    ("GRU", "JFK", "2026-12-13", 3500),
    ("JFK", "MIA", "2026-12-22", 800),
    ("MIA", "GRU", "2027-01-10", 3500)
]

def buscar_preco(origem, destino, data):
    url = f"https://www.skyscanner.com.br/transport/flights/{origem}/{destino}/{data}/"
    
    print(f"\n🔍 {origem} → {destino} | {data}")
    print(f"🌐 Ver direto: {url}")
    
    # valor simulado mais realista
    preco_estimado = 3000
    
    return preco_estimado

def monitorar():
    for origem, destino, data, limite in ROTAS:
        preco = buscar_preco(origem, destino, data)
        
        print(f"💰 Estimativa: R$ {preco}")
        
        if preco < limite:
            print("🔥 PROMOÇÃO!")
        else:
            print("❌ Ainda caro")

monitorar()
