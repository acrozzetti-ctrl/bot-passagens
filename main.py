import json
import os

ROTAS = [
    ("GRU", "JFK", "2026-12-11", 3500),
    ("GRU", "JFK", "2026-12-12", 3500),
    ("GRU", "JFK", "2026-12-13", 3500),
    ("GRU", "JFK", "2026-12-14", 3500),

    ("JFK", "MIA", "2026-12-22", 800),

    ("MIA", "GRU", "2027-01-09", 3500),
    ("MIA", "GRU", "2027-01-10", 3500),
    ("MIA", "GRU", "2027-01-11", 3500)
]

ARQUIVO = "precos.json"

def carregar_precos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return {}

def salvar_precos(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)

def buscar_preco_fake():
    import random
    return random.randint(2000, 5000)

def monitorar():
    historico = carregar_precos()
    novos_dados = {}

    for origem, destino, data, limite in ROTAS:
        chave = f"{origem}-{destino}-{data}"
        
        preco = buscar_preco_fake()
        antigo = historico.get(chave)

        print(f"\n🔍 {origem} → {destino} | {data}")
        print(f"💰 Atual: R$ {preco}")

        if antigo:
            print(f"📉 Antes: R$ {antigo}")

            if preco < antigo:
                print("🔥 BAIXOU DE PREÇO!")
            
            if preco < limite:
                print("🚨 PROMOÇÃO REAL!")

        novos_dados[chave] = preco

    salvar_precos(novos_dados)

monitorar()
