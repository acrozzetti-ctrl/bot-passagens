def salvar_arquivo(dados, sha):
    url = f"https://api.github.com/repos/{REPO}/contents/{ARQUIVO}"
    headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

    conteudo = base64.b64encode(json.dumps(dados, indent=2).encode()).decode()

    body = {
        "message": "Atualizando preços automaticamente",
        "content": conteudo
    }

    if sha:
        body["sha"] = sha

    r = requests.put(url, headers=headers, json=body)
    
    print("STATUS SALVAR:", r.status_code)
    print(r.text)
monitorar()
