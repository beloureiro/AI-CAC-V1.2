import os
from datetime import datetime  # Adiciona a biblioteca para trabalhar com data e hora
from utils import load_yaml_file, load_feedback, send_request

class FeedbackAnalyzer:
    def __init__(self, config_path, feedback_path, agents_path):
        # Carregar as configurações do arquivo YAML
        self.config = load_yaml_file(config_path)
        
        # Carregar o feedback do arquivo de texto
        self.feedback = load_feedback(feedback_path)

        # Carregar os agentes do arquivo YAML
        self.agents = load_yaml_file(agents_path)['agents']

        # Configurações da API do modelo
        self.url = self.config['server']['url']
        self.model = self.config['request']['model']['gemma-2-9b-it-GGUF']
        self.headers = {"Content-Type": "application/json"}

    def analyze_with_agent(self, agent_prompt, max_tokens, temperature):
        # Substituir o espaço reservado "[feedback]" com o feedback real
        prompt_with_feedback = agent_prompt.replace("[feedback]", self.feedback)
        # Enviar a solicitação ao modelo
        return send_request(self.url, self.headers, self.model, prompt_with_feedback, max_tokens, temperature)

    def run_analysis(self):
        # Dicionário para armazenar os resultados de cada agente
        results = {}

        # Executar cada agente e coletar as respostas
        for agent_name, agent_data in self.agents.items():
            print(f"Running analysis for {agent_name}...")

            # Extrair o prompt, max_tokens e temperatura do YAML
            prompt = agent_data['prompt']
            max_tokens = agent_data.get('max_tokens')
            temperature = agent_data.get('temperature')

            # Verifica se max_tokens e temperature estão definidos para o agente, senão lança um erro
            if max_tokens is None or temperature is None:
                raise ValueError(f"Agente {agent_name} não tem 'max_tokens' ou 'temperature' definidos no YAML.")

            # Fazer a análise com o agente
            result = self.analyze_with_agent(prompt, max_tokens, temperature)
            results[agent_name] = result

            print(f"{agent_name} result: \n{result}\n")
        
        return results

    def save_results_to_md(self, results):
        # Pega a data e hora atuais
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define o caminho do arquivo .md com base na pasta especificada e no formato "report_data_hora.md"
        md_file_path = os.path.join(
            "D:/OneDrive - InMotion - Consulting/AI Projects/AI-CAC-V1.2/LmStudio/lms_reports_md", 
            f'report_{current_time}.md'
        )

        # Abrir o arquivo em modo de escrita (criar ou sobrescrever)
        with open(md_file_path, 'w', encoding='utf-8') as file:
            file.write("# Feedback Analysis Report\n\n")
            file.write("This report contains the analysis results for each expert agent based on the patient's feedback.\n\n")
            
            for agent, result in results.items():
                file.write(f"## {agent}\n\n")
                file.write(f"```\n{result}\n```\n\n")

        print(f"Results saved to {md_file_path}")

# Caminhos dos arquivos
config_path = "config/local_llm.yaml"
feedback_path = "D:/OneDrive - InMotion - Consulting/AI Projects/AI-CAC-V1.2/patient_feedback.txt"
agents_path = "LmStudio/lm_agents.yaml"

# Instanciar o analisador de feedback
analyzer = FeedbackAnalyzer(config_path, feedback_path, agents_path)

# Executar a análise
resultados = analyzer.run_analysis()

# Salvar os resultados no arquivo .md
analyzer.save_results_to_md(resultados)
