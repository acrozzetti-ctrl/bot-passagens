import requests

API_KEY = "SUA_API_KEY_AQUI"

url = "https://api.tequila.kiwi.com/v2/search"

headers = {
    "apikey": API_KEY
}

params = {
    "fly_from": "GRU",
    "fly_to": "JFK",
    "date_from": "13/12/2026",
    "date_to": "13/12/2026",
    "curr": "BRL",
    "limit": 1
}

r = requests.get(url, headers=headers, params=params)

print("STATUS:", r.status_code)
print(r.json())
