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

def buscar_voo(origem, destino):
    url = "https://google-flights-data.p.rapidapi.com/flights/search-oneway"

    params = {
        "departureId": origem,
        "arrivalId": destino
    }

    try:
        r = requests.get(url, headers=HEADERS, params=params)
        data = r.json()

        # DEBUG (pode tirar depois)
        print(json.dumps(data, indent=2))

        itinerarios = data.get("data", {}).get("itineraries", [])

        if not itinerarios:
            return None

        voo = itinerarios[0]

        preco = voo.get("price", {}).get("raw")

        legs = voo.get("legs", [])
        if not legs:
            return None

        leg = legs[0]

        companhia = (
            leg.get("carriers", {})
               .get("marketing", [{}])[0]
               .get("name", "Não informado")
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
        "message": "Atualizando voos (seguro)",
        "content": conteudo
    }

    if sha:
        body["sha"] = sha

    r = requests.put(url, headers=headers, json=body)

    print("STATUS:", r.status_code)


def monitorar():
    historico, sha = carregar_arquivo()

    for origem, destino, data in ROTAS:
        chave = f"{origem}-{destino}-{data}"

        print(f"\n🔍 {origem} → {destino}")

        voo = buscar_voo(origem, destino)

        if voo and voo["preco"]:
            if chave not in historico:
                historico[chave] = []

            historico[chave].append(voo)

            print("✅ OK:", voo)
        else:
            print("⚠️ Sem dados dessa rota")

    salvar_arquivo(historico, sha)


monitorar()
