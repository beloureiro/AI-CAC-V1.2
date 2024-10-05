import os
import json
import logging

class DbIntegration:
    def __init__(self, json_directory):
        self.json_directory = json_directory
        
        # Configurar o logging
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

    def process_json_report(self, file_path):
        """
        Processa um arquivo JSON contendo o feedback do paciente e as respostas dos agentes,
        retornando um dicionário organizado para cada agente.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
        except Exception as e:
            logging.error(f"Erro ao ler o arquivo {file_path}: {e}")
            return None

        logging.debug(f"Arquivo JSON lido com sucesso: {file_path}")

        # Inicializa o dicionário de dados com strings vazias
        data = {key: "" for key in [
            "Feedback_ID",
            "Total_execution_time",
            "Patient_Feedback",
            "Sentiment_Patient_Experience_Expert",
            "Emotional_Intensity_Patient_Experience_Expert",
            "Urgency_Level_Patient_Experience_Expert",
            "Key_Issues_Patient_Experience_Expert",
            "Patient_Journey_Health_IT_Process_Expert",
            "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert",
            "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert",
            "Emotional_State_Clinical_Psychologist",
            "Support_Strategy_Clinical_Psychologist",
            "Suggested_Approach_Clinical_Psychologist",
            "Communication_Quality_Communication_Expert",
            "Issues_Identified_Communication_Expert",
            "Suggested_Improvements_Communication_Expert",
            "Final_Recommendation_Communication_Expert",
            "Key_Issues_Manager_and_Advisor",
            "Recommendations_Manager_and_Advisor"
        ]}

        # Use o nome do arquivo como Feedback_ID
        feedback_id = os.path.basename(file_path).split('.')[0]
        data["Feedback_ID"] = feedback_id

        # Extrai 'Total_execution_time' e 'Patient_Feedback'
        data["Total_execution_time"] = content.get("total_execution_time", "")
        data["Patient_Feedback"] = content.get("patient_feedback", "")

        # Processa a resposta de cada agente
        for agent in content.get("agents", []):
            agent_name = agent["agent_name"].lower().replace(' ', '_')
            response = agent.get("response", {})

            # Garantir que 'response' seja sempre um dicionário
            if isinstance(response, str):
                try:
                    response = json.loads(response)
                except json.JSONDecodeError:
                    response = {}  # Se a conversão falhar, usar um dicionário vazio

            logging.debug(f"Processando agente: {agent_name} no arquivo {file_path}")

            if "patient_experience_expert" in agent_name:
                self.extract_patient_experience_expert(response, data)
            elif "health_it_process_expert" in agent_name:
                self.extract_health_it_process_expert(response, data)
            elif "clinical_psychologist" in agent_name:
                self.extract_clinical_psychologist(response, data)
            elif "communication_expert" in agent_name:
                self.extract_communication_expert(response, data)
            elif "manager_and_advisor" in agent_name:
                self.extract_manager_and_advisor(response, data)

        return data

    def extract_patient_experience_expert(self, response, data):
        """Extrai informações do agente 'Patient Experience Expert'."""
        logging.debug("Extraindo informações de 'Patient Experience Expert'")
        data["Sentiment_Patient_Experience_Expert"] = response.get("Sentiment_Patient_Experience_Expert", "").strip()
        data["Emotional_Intensity_Patient_Experience_Expert"] = response.get("Emotional_Intensity_Patient_Experience_Expert", "").strip()
        data["Urgency_Level_Patient_Experience_Expert"] = response.get("Urgency_Level_Patient_Experience_Expert", "").strip()

        key_issues = response.get("Key_Issues_Patient_Experience_Expert", "").strip()
        if key_issues:
            key_issues_list = key_issues.split("; ")
            data["Key_Issues_Patient_Experience_Expert"] = "; ".join(key_issues_list)
        else:
            data["Key_Issues_Patient_Experience_Expert"] = ""

    def extract_health_it_process_expert(self, response, data):
        """Extrai informações do agente 'Health & IT Process Expert'."""
        logging.debug("Extraindo informações de 'Health & IT Process Expert'")

        # Captura e processa os dados separando-os por ponto e vírgula
        data["Patient_Journey_Health_IT_Process_Expert"] = self.process_expert_field(
            response.get("Patient_Journey_Health_IT_Process_Expert", "")
        )
        data["Inefficiencies_Healthcare_Process_Health_IT_Process_Expert"] = self.process_expert_field(
            response.get("Inefficiencies_Healthcare_Process_Health_IT_Process_Expert", "")
        )
        data["Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert"] = self.process_expert_field(
            response.get("Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert", "")
        )

    def process_expert_field(self, field_value):
        """
        Processa o campo do especialista, separando os valores por ponto e vírgula e 
        removendo espaços extras.
        """
        if field_value:
            # Divide o campo por '; ' e remove espaços extras
            return "; ".join([item.strip() for item in field_value.strip("; ").split(";") if item.strip()])
        return ""


    def extract_clinical_psychologist(self, response, data):
        """Extrai informações do agente 'Clinical Psychologist'."""
        logging.debug("Extraindo informações de 'Clinical Psychologist'")
        data["Emotional_State_Clinical_Psychologist"] = response.get("Emotional_State_Clinical_Psychologist", "").strip()
        data["Support_Strategy_Clinical_Psychologist"] = response.get("Support_Strategy_Clinical_Psychologist", "").strip()

        suggested_approach = response.get("Suggested_Approach_Clinical_Psychologist", "").strip()
        if suggested_approach:
            suggested_approach_list = suggested_approach.split("; ")
            data["Suggested_Approach_Clinical_Psychologist"] = "; ".join(suggested_approach_list)
        else:
            data["Suggested_Approach_Clinical_Psychologist"] = ""

    def extract_communication_expert(self, response, data):
        """Extrai informações do agente 'Communication Expert'."""
        logging.debug("Extraindo informações de 'Communication Expert'")
        data["Communication_Quality_Communication_Expert"] = response.get("Communication_Quality_Communication_Expert", "").strip()
        data["Final_Recommendation_Communication_Expert"] = response.get("Final_Recommendation_Communication_Expert", "").strip()

        issues_identified = response.get("Issues_Identified_Communication_Expert", "").strip()
        suggested_improvements = response.get("Suggested_Improvements_Communication_Expert", "").strip()

        if issues_identified:
            issues_list = issues_identified.split("; ")
            data["Issues_Identified_Communication_Expert"] = "; ".join(issues_list)
        else:
            data["Issues_Identified_Communication_Expert"] = ""

        if suggested_improvements:
            improvements_list = suggested_improvements.split("; ")
            data["Suggested_Improvements_Communication_Expert"] = "; ".join(improvements_list)
        else:
            data["Suggested_Improvements_Communication_Expert"] = ""

    def extract_manager_and_advisor(self, response, data):
        """Extrai informações do agente 'Manager and Advisor'."""
        logging.debug("Extraindo informações de 'Manager and Advisor'")
        key_issues = response.get("Key_Issues_Manager_and_Advisor", "").strip()
        recommendations = response.get("Recommendations_Manager_and_Advisor", "").strip()

        if key_issues:
            key_issues_list = key_issues.split("; ")
            data["Key_Issues_Manager_and_Advisor"] = "; ".join(key_issues_list)
        else:
            data["Key_Issues_Manager_and_Advisor"] = ""

        if recommendations:
            recommendations_list = recommendations.split("; ")
            data["Recommendations_Manager_and_Advisor"] = "; ".join(recommendations_list)
        else:
            data["Recommendations_Manager_and_Advisor"] = ""

    def process_multiple_jsons(self):
        """
        Processa múltiplos arquivos JSON no diretório especificado.
        """
        for file_name in os.listdir(self.json_directory):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.json_directory, file_name)
                data = self.process_json_report(file_path)
                if data:
                    logging.info(f"Processado com sucesso: {file_name}")

        print("Finished processing all JSON files.")

if __name__ == "__main__":
    # Caminhos e diretórios
    directory_with_jsons = "D:\\OneDrive - InMotion - Consulting\\AI Projects\\AI-CAC-V1.2\\data_reports_json"

    # Criar uma instância da classe DbIntegration
    db_integration = DbIntegration(directory_with_jsons)

    # Processar os arquivos JSON
    db_integration.process_multiple_jsons()
