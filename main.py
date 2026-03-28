import requests
import json
import base64
import os

TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
ARQUIVO = "precos.json"

API_KEY = os.getenv("RAPIDAPI_KEY")

print("🔑 API KEY:", "OK" if API_KEY else "ERRO")

HEADERS = {
    "x-rapidapi-host": "google-flights-data.p.rapidapi.com",
    "x-rapidapi-key": API_KEY
}

ROTAS = [
    ("JFK", "LHR"),
    ("JFK", "MIA"),
    ("MIA", "GRU")
]

def buscar_voo(origem, destino):
    url = "https://google-flights-data.p.rapidapi.com/flights/search-oneway"

    params = {
        "departureId": origem,
        "arrivalId": destino
    }

    r = requests.get(url, headers=HEADERS, params=params)

    print(f"🌐 STATUS API ({origem}-{destino}):", r.status_code)

    try:
        data = r.json()

        itinerarios = data.get("data", {}).get("itineraries", [])

        if not itinerarios:
            return None

        voo = itinerarios[0]

        preco = voo.get("price", {}).get("raw")

        leg = voo.get("legs", [{}])[0]

        companhia = (
            leg.get("carriers", {})
               .get("marketing", [{}])[0]
               .get("name", "N/A")
        )

        saida = leg.get("departure", "-")
        chegada = leg.get("arrival", "-")

        return {
            "preco": preco,
            "companhia": companhia,
            "saida": saida,
            "chegada": chegada
        }

    except Exception as e:
        print("Erro:", e)
        print(r.text)
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
        "message": "Atualizando voos RapidAPI",
        "content": conteudo
    }

    if sha:
        body["sha"] = sha

    r = requests.put(url, headers=headers, json=body)

    print("💾 STATUS SALVAR:", r.status_code)


def monitorar():
    historico, sha = carregar_arquivo()

    for origem, destino in ROTAS:
        chave = f"{origem}-{destino}"

        print(f"\n🔍 {origem} → {destino}")

        voo = buscar_voo(origem, destino)

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

    salvar_arquivo(historico, sha)


monitorar()
