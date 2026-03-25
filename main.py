import random

ROTAS = [
    ("GRU", "JFK", "13/12/2026", 3500),
    ("JFK", "MIA", "22/12/2026", 800),
    ("MIA", "GRU", "10/01/2027", 3500)
]

def buscar_precos():
    for origem, destino, data, limite in ROTAS:
        print(f"\n🔍 {origem} → {destino} | {data}")
        
        # simulação de preço (vamos trocar depois por real)
        preco = random.randint(2000, 5000)
        
        print(f"💰 Preço: R$ {preco}")
        
        if preco < limite:
            print("🔥 PROMOÇÃO ENCONTRADA!")
        else:
            print("❌ Ainda caro")

buscar_precos()
