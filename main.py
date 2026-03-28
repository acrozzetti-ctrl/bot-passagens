import requests
import json
import base64
import os

TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
ARQUIVO = "precos.json"

API_KEY = os.getenv("RAPIDAPI_KEY")

HEADERS = {
    "x-rapidapi-host": "google-flights-data.p.rapidapi.com",
    "x-rapidapi-key": API_KEY
}

ROTAS = [
    ("GRU", "JFK", "2026-12-13"),
    ("JFK", "MIA", "2026-12-22"),
    ("MIA", "GRU", "2027-01-10")
]

def buscar_preco(origem, destino):
    url = "https://google-flights-data.p.rapidapi.com/flights/search-oneway"
    
    params = {
        "departureId": origem,
        "arrivalId": destino
    }

    r = requests.get(url, headers=HEADERS, params=params)
    data = r.json()

    try:
        preco = data["data"]["itineraries"][0]["price"]["raw"]
        return int(preco)
    except:
        print("Erro ao pegar preço:", data)
        return None


def carregar_arquivo():
    url = f"https://api.github.com/repos/{REPO}/contents/{ARQUIVO}"

    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        conteudo = r.json()
        dados = json.loads(base64.b64decode(conteudo["content"]).decode())
        return dados, conteudo["sha"]
    else:
        return {}, None


def salvar_arquivo(dados, sha):
    url = f"https://api.github.com/repos/{REPO}/contents/{ARQUIVO}"

    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    conteudo = base64.b64encode(json.dumps(dados, indent=2).encode()).decode()

    body = {
        "message": "Atualizando preços com API real",
        "content": conteudo
    }

    if sha:
        body["sha"] = sha

    r = requests.put(url, headers=headers, json=body)

    print("STATUS SALVAR:", r.status_code)
    print(r.text)


def monitorar():
    historico, sha = carregar_arquivo()

    for origem, destino, data in ROTAS:
        chave = f"{origem}-{destino}-{data}"

        print(f"\n🔍 {origem} → {destino}")

        preco = buscar_preco(origem, destino)

        if preco:
            print(f"💰 Preço encontrado: R$ {preco}")

            if chave not in historico:
                historico[chave] = []

            if isinstance(historico[chave], int):
                historico[chave] = [historico[chave]]

            historico[chave].append(preco)

    salvar_arquivo(historico, sha)


monitorar()
