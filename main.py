import json
import requests
import base64
import os
import random

ROTAS = [
    ("GRU", "JFK", "2026-12-13", 3000),
    ("JFK", "MIA", "2026-12-22", 800),
    ("MIA", "GRU", "2027-01-10", 3200)
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
        "content": conteudo
    }

    if sha:
        body["sha"] = sha

    r = requests.put(url, headers=headers, json=body)

    print("STATUS SALVAR:", r.status_code)

def buscar_preco_realista(origem, destino):
    base = {
        ("GRU", "JFK"): 3200,
        ("JFK", "MIA"): 700,
        ("MIA", "GRU"): 3000
    }

    preco_base = base.get((origem, destino), 2500)
    variacao = random.randint(-800, 800)

    return max(500, preco_base + variacao)

def monitorar():
    historico, sha = pegar_arquivo()

    for origem, destino, data, limite in ROTAS:
        chave = f"{origem}-{destino}-{data}"
        
        preco = buscar_preco_realista(origem, destino)

       # se não existir, cria lista
if chave not in historico:
    historico[chave] = []

# se for número antigo, transforma em lista
if isinstance(historico[chave], int):
    historico[chave] = [historico[chave]]

# agora adiciona normalmente
historico[chave].append(preco)

        print(f"\n🔍 {origem} → {destino} | {data}")
        print(f"💰 Atual: R$ {preco}")

        if preco < limite:
            print("🔥 PROMOÇÃO REAL!")

    salvar_arquivo(historico, sha)

monitorar()
