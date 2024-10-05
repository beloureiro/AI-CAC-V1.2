import requests
import json
import yaml

def load_yaml_file(filepath):
    """Carregar arquivos YAML."""
    with open(filepath, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def load_feedback(filepath):
    """Carregar feedback de um arquivo de texto."""
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def send_request(url, headers, model, prompt, max_tokens, temperature):
    """Enviar a requisição POST para o modelo."""
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    # Fazer a requisição POST
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Verificar o status da resposta
    if response.status_code == 200:
        completion = response.json()
        return completion['choices'][0]['text']
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)
        return None
