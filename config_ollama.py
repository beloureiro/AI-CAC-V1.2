import os

# Set a dummy OpenAI API key (required for initialization, even if not used)
os.environ["OPENAI_API_KEY"] = "sk-proj-111"

# Configure the Ollama local models
#----------------------------------
llama_3_1_8b_instruct_q8_0= "ollama/llama3.1:8b-instruct-q8_0"
llama_3_1_8b_instruct_q5_K_S = "ollama/llama3.1:8b-instruct-q5_K_S"
llama3_2_3b_instruct_q5_K_S = "ollama/llama3.2:3b-instruct-q5_K_S"
llama3_2_1b_instruct_q5_K_S = "ollama/llama3.2:1b-instruct-q5_K_S"
llama3_2_latest = "ollama/llama3.2:latest"
llama3_1_8b = "ollama/llama3.1:8b " 
gemma2_27b_instruct_q2_K  = "ollama/gemma2:27b-instruct-q2_K " # castiga hardware
gemma2_9b_instruct_q5_K_S = "ollama/gemma2:9b-instruct-q5_K_S"
gemma2_9b_instruct_q8_0 = "ollama/gemma2:9b-instruct-q8_0"
gemma2_2b_text_q5_K_S = "ollama/gemma2:2b-instruct-q5_K_S"
gemma2_2b_instruct_q4_K_S = "ollama/gemma2:2b-instruct-q4_K_S"
mistral12b_model = "ollama/mistral-nemo:12b-instruct-2407-q3_K_M" # castiga hardware
mistral_nemo_12b_instruct_2407_q8_0 = "ollama/mistral-nemo:12b-instruct-2407-q8_0" # castiga hardware
mistral_nemo_12b_instruct_2407_q5_K_S = "ollama/mistral-nemo:12b-instruct-2407-q5_K_S"
nomic_text_model = "ollama/nomic-embed-text:latest"
mxbai_text_model = "ollama/mxbai-embed-large:latest"
phi3_5_3_8b_mini_instruct_q8_0 = "ollama/phi3.5:3.8b-mini-instruct-q8_0"
qwen2_5_7b_instruct_q8_0 = "ollama/qwen2.5:7b-instruct-q8_0"
#----------------------------------
