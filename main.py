import requests
import json
import base64
import os

TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
ARQUIVO = "precos.json"

API_KEY = os.getenv("TEQUILA_API_KEY")

ROTAS = [
    ("GRU", "JFK", "10/05/2026"),
    ("JFK", "MIA", "15/05/2026"),
    ("MIA", "GRU", "20/05/2026")
]

def buscar_voo(origem, destino, data):
    url = "https://api.tequila.kiwi.com/v2/search"

    headers = {
        "apikey": RAPIDAPI_KEY
    }

    params = {
        "fly_from": origem,
        "fly_to": destino,
        "date_from": data,
        "date_to": data,
        "curr": "BRL",
        "limit": 1,
        "sort": "price"
    }

    r = requests.get(url, headers=headers, params=params)

    try:
        data = r.json()

        if not data.get("data"):
            return None

        voo = data["data"][0]

        return {
            "preco": voo.get("price"),
            "companhia": voo.get("airlines", ["-"])[0],
            "saida": voo.get("local_departure", "-"),
            "chegada": voo.get("local_arrival", "-")
        }

    except:
        print("Erro API:", r.text)
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
        "message": "Atualizando voos reais (Kiwi)",
        "content": conteudo
    }

    if sha:
        body["sha"] = sha

    requests.put(url, headers=headers, json=body)


def monitorar():
    historico, sha = carregar_arquivo()

    for origem, destino, data in ROTAS:
        chave = f"{origem}-{destino}-{data}"

        print(f"\n🔍 {origem} → {destino} | {data}")

        voo = buscar_voo(origem, destino, data)

        if chave not in historico:
            historico[chave] = []

        if voo:
            historico[chave].append(voo)
            print("✅ OK:", voo)
        else:
            historico[chave].append({
                "preco": None,
                "companhia": "Sem dados",
                "saida": "-",
                "chegada": "-"
            })
            print("⚠️ Sem voo encontrado")

    salvar_arquivo(historico, sha)


monitorar()
