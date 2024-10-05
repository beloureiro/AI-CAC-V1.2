from crewai_tools import BaseTool
from typing import ClassVar
import re

# Health & IT Process Expert Agent Class
class HealthITProcessExpertAgent(BaseTool):
    name: str = "Health IT Process Expert"
    description: str = "Maps the patient's journey based on feedback and suggests improvements using BPMN principles."
    
    args: ClassVar[dict] = {
        "feedback": {
            "title": "Feedback",
            "type": "string",
            "description": "The patient feedback that the agent will analyze to map the process and suggest improvements."
        }
    }

    def map_patient_journey(self, feedback: str) -> list:
        """
        Extracts the steps of the patient's journey from the feedback, following the BPMN structure.
        """
        journey_steps = []

        # Estrutura geral para mapear o processo com base em BPMN
        sentences = feedback.split(".")
        
        # Evento de início do processo
        journey_steps.append("Start Event: The process begins with patient interaction, such as searching or scheduling an appointment.")

        # Analisando cada sentença para detectar atividades, gateways e eventos
        for sentence in sentences:
            sentence = sentence.strip().lower()

            # Detectar atividades e eventos no feedback
            if "appointment" in sentence:
                journey_steps.append("Task: Patient schedules an appointment.")
            elif "wait" in sentence or "delayed" in sentence:
                journey_steps.append("Intermediate Event: Waiting or delay in the process.")
            elif "denied" in sentence or "turned away" in sentence:
                journey_steps.append("Gateway: Decision to deny service or redirect patient.")
            elif "payment" in sentence:
                journey_steps.append("Task: Patient makes a payment.")
            elif "consultation" in sentence:
                journey_steps.append("Task: Patient attends consultation (online or offline).")
            elif "review" in sentence or "feedback" in sentence:
                journey_steps.append("End Event: Patient provides feedback and completes the process.")

        # Transições e fluxos de sequência entre as atividades e eventos
        journey_steps = self.add_sequence_flows(journey_steps)

        # Evento de fim, caso não tenha sido capturado
        if not any("end event" in step.lower() for step in journey_steps):
            journey_steps.append("End Event: The process ends with the patient's feedback or conclusion of the consultation.")

        return journey_steps

    def add_sequence_flows(self, steps: list) -> list:
        """
        Add sequence flows between elements in the BPMN structure.
        """
        sequenced_steps = []
        for i, step in enumerate(steps):
            sequenced_steps.append(step)
            if i < len(steps) - 1:
                sequenced_steps.append(f"Sequence Flow: Transition from '{steps[i]}' to '{steps[i+1]}'.")
        return sequenced_steps

    def identify_inefficiencies(self, feedback: str) -> list:
        """
        Identifies inefficiencies in the process based on the patient's feedback.
        """
        inefficiencies = []

        # Verificar por problemas estruturais no processo
        if "wait" in feedback or "delayed" in feedback:
            inefficiencies.append("Process inefficiency: Long waiting time or delays.")
        if "denied" in feedback or "turned away" in feedback:
            inefficiencies.append("Process inefficiency: Patient denied service or treatment.")
        if "rude" in feedback or "disrespectful" in feedback:
            inefficiencies.append("Process inefficiency: Poor communication or unprofessional behavior by staff.")
        if "no treatment" in feedback or "no resolution" in feedback:
            inefficiencies.append("Process inefficiency: Lack of resolution or inadequate treatment.")

        if not inefficiencies:
            inefficiencies.append("No inefficiencies identified in the process.")

        return inefficiencies

    def propose_improvements(self, inefficiencies: list) -> list:
        """
        Suggests improvements based on the identified inefficiencies.
        """
        improvements = []

        # Sugerir melhorias com base nas ineficiências detectadas
        for inefficiency in inefficiencies:
            if "waiting time" in inefficiency:
                improvements.append("Improve scheduling and reduce waiting times.")
            if "denied service" in inefficiency:
                improvements.append("Review patient triage process to ensure proper treatment is provided.")
            if "poor communication" in inefficiency:
                improvements.append("Implement communication training for staff to improve professionalism.")
            if "lack of resolution" in inefficiency:
                improvements.append("Ensure follow-up procedures are in place for unresolved cases.")

        if not improvements:
            improvements.append("No improvements needed.")

        return improvements

    def _run(self, feedback: str) -> dict:  # Ajuste para seguir o padrão do framework
        """
        Runs the agent to process the feedback and return the mapped journey, inefficiencies, and improvements.
        """
        # Map the patient's journey
        journey = self.map_patient_journey(feedback)

        # Identify inefficiencies
        inefficiencies = self.identify_inefficiencies(feedback)

        # Propose improvements
        improvements = self.propose_improvements(inefficiencies)

        # Format the final output
        result = {
            "Patient_Journey_Health_IT_Process_Expert": "\n".join(journey),
            "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert": "\n".join(inefficiencies),
            "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert": "\n".join(improvements)
        }

        return result

# Output Validator for Health & IT Process Expert
class HealthITProcessExpertOutputValidatorTool(BaseTool):
    name: str = "Health IT Process Expert Output Validator"
    description: str = "Validates and formats the output of the Health & IT Process Expert to ensure proper structure."

    def _run(self, response: str) -> dict:
        formatted_data = {
            "Patient_Journey_Health_IT_Process_Expert": "",
            "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert": "",
            "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert": ""
        }

        # Process and validate the response, splitting it by lines
        current_field = None
        lines = response.split('\n')

        for line in lines:
            line = line.strip()  # Remove extra spaces

            # Check if the line contains the field title
            if "Patient_Journey_Health_IT_Process_Expert" in line:
                current_field = "Patient_Journey_Health_IT_Process_Expert"
                continue
            elif "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert" in line:
                current_field = "Inefficiencies_Healthcare_Process_Health_IT_Process_Expert"
                continue
            elif "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert" in line:
                current_field = "Improvement_Suggestions_Healthcare_Process_Health_IT_Process_Expert"
                continue

            # Append content to the current field
            if current_field and line:
                if formatted_data[current_field]:
                    formatted_data[current_field] += f"\n- {line}"
                else:
                    formatted_data[current_field] = f"- {line}"

        return formatted_data


# Output Validator for Clinical Psychologist
class ClinicalPsychologistOutputValidatorTool(BaseTool):
    name: str = "Clinical Psychologist Output Validator"
    description: str = "Validates and formats the output of the Clinical Psychologist agent to ensure proper structure without altering empty values."

    def _run(self, response: str) -> dict:
        formatted_data = {
            "Emotional_State_Clinical_Psychologist": "",
            "Support_Strategy_Clinical_Psychologist": "",
            "Suggested_Approach_Clinical_Psychologist": ""
        }

        bold_pattern = re.compile(r'\*\*(.*?)\*\*')
        italic_pattern = re.compile(r'\*(.*?)\*')

        # Process the response line by line
        lines = response.split('\n')
        current_field = None
        list_items = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Handle bold and italic formatting
            line = bold_pattern.sub(r'\1', line)
            line = italic_pattern.sub(r'\1', line)

            # Check for key-value pairs (field: value)
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                if key in formatted_data:
                    formatted_data[key] = value
                    current_field = key
                    list_items = []
                else:
                    current_field = None
            # Handle list items
            elif line.startswith('-') and current_field:
                item = line.strip('- ').strip()
                list_items.append(item)
                formatted_data[current_field] = '\n'.join(list_items)

        return formatted_data
