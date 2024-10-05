import requests
import json

# Defina o endpoint do LM Studio
url = "http://127.0.0.1:1234/v1/completions"

# Defina os parâmetros da solicitação
payload = {
    "model": "meta-llama-3.1-8b-instruct",  # Nome do modelo fornecido
    "prompt": "Explique a teoria da relatividade de forma simples.",
    "max_tokens": 250,  # Defina o número máximo de tokens na resposta
    "temperature": 0  # Controle de aleatoriedade na geração de texto
}

# Defina os cabeçalhos da solicitação
headers = {
    "Content-Type": "application/json"
}

# Faça a solicitação POST
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Verifique o status da resposta
if response.status_code == 200:
    completion = response.json()
    print("Resposta do modelo:", completion['choices'][0]['text'])
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
