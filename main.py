import requests

ROTAS = [
    ("GRU", "JFK", "13/12/2026"),
    ("JFK", "MIA", "22/12/2026"),
    ("MIA", "GRU", "10/01/2027")
]

def buscar_precos():
    for origem, destino, data in ROTAS:
        print(f"\n🔍 Buscando: {origem} → {destino} | {data}")
        
        # simulação de preço (depois a gente melhora)
        preco = 2500
        
        print(f"💰 Preço encontrado: R$ {preco}")

buscar_precos()
