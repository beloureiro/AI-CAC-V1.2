import time
import os
from crew_advisory import ai_clinical_crew
from utils import (
    log_model_usage, get_patient_feedback, log_all_models, 
    format_task_descriptions, execute_agents, 
    save_consolidated_report, save_agent_results_as_json  # Importa a função de salvar JSON
)
from Db_integration import DbIntegration  # Importe a nova classe

def execute_crew():
    start_time = time.time()  # Início da execução

    # Pega o feedback do paciente
    patient_feedback = get_patient_feedback()

    # Imprime o relatório inicial no terminal
    print("############################")
    print("# AI Clinical Advisory Crew Report")
    print("############################\n")
    print(f"Patient Feedback for Analysis:\n{patient_feedback}\n")

    # Ajusta as descrições das tarefas com base no feedback do paciente
    format_task_descriptions(ai_clinical_crew.tasks, patient_feedback)

    # Loga os modelos LLM usados pelos agentes
    print("LLM Models Used by Agents:\n")
    agents = [task.agent for task in ai_clinical_crew.tasks]
    log_all_models(agents)

    # Executa as tarefas dos agentes com o feedback do paciente
    result = ai_clinical_crew.kickoff(inputs={"feedback": patient_feedback})

    # Executa os agentes e imprime os resultados no terminal
    execute_agents(result.tasks_output)

    # Calcula a duração total da execução
    end_time = time.time()
    total_duration = end_time - start_time

    # Imprime o relatório consolidado final
    print("############################")
    print("# Consolidated Final Report")
    print("############################\n")
    print(f"Patient Feedback: {patient_feedback}\n")

    # Usa caminhos relativos para os diretórios
    base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_directory = os.path.join(base_dir, "data_reports_txt")
    json_directory = os.path.join(base_dir, "data_reports_json")

    # Garante que os diretórios existam
    os.makedirs(txt_directory, exist_ok=True)
    os.makedirs(json_directory, exist_ok=True)

    # Salva o relatório consolidado em um arquivo de texto
    report_file_name = save_consolidated_report(patient_feedback, result.tasks_output, total_duration, txt_directory)
    print(f"Report saved as: {report_file_name}")

    # Salva o relatório consolidado em um arquivo JSON
    report_json_name = save_agent_results_as_json(patient_feedback, result.tasks_output, total_duration, json_directory)
    print(f"Report saved as JSON: {report_json_name}")

    # Processa os arquivos JSON
    db_integration = DbIntegration(json_directory)
    db_integration.process_multiple_jsons()

if __name__ == "__main__":
    execute_crew()
