import json
import requests
import base64
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

REPO = os.getenv("GITHUB_REPOSITORY")
TOKEN = os.getenv("GITHUB_TOKEN")
ARQUIVO = "precos.json"

def pegar_arquivo():
    url = f"https://api.github.com/repos/{REPO}/contents/{ARQUIVO}"
    headers = {"Authorization": f"token {TOKEN}"}

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        conteudo = r.json()
        dados = base64.b64decode(conteudo["content"]).decode()
        return json.loads(dados), conteudo["sha"]
    
    return {}, None

def salvar_arquivo(dados, sha):
    url = f"https://api.github.com/repos/{REPO}/contents/{ARQUIVO}"
    headers = {"Authorization": f"token {TOKEN}"}

    conteudo = base64.b64encode(json.dumps(dados, indent=2).encode()).decode()

    body = {
        "message": "Atualizando preços automaticamente",
        "content": conteudo,
        "sha": sha
    }

    requests.put(url, headers=headers, json=body)

def buscar_preco_fake():
    import random
    return random.randint(2000, 5000)

def monitorar():
    historico, sha = pegar_arquivo()
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

    salvar_arquivo(novos_dados, sha)

monitorar()
