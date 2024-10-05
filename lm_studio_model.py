import requests
import json
import yaml

# Carregar as configurações do arquivo YAML
with open("config/local_llm.yaml", "r") as file:
    config = yaml.safe_load(file)

# Definir o endpoint e os parâmetros a partir do YAML
url = config['server']['url']

payload = {
    "model": config['request']['model'],
    "prompt": config['request']['prompt'],
    "max_tokens": config['request']['max_tokens'],
    "temperature": config['request']['temperature']
}

# Definir os cabeçalhos da solicitação
headers = {
    "Content-Type": "application/json"
}

# Fazer a solicitação POST
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Verificar o status da resposta
if response.status_code == 200:
    completion = response.json()
    print("Resposta do modelo:", completion['choices'][0]['text'])
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
