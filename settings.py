import os

USE_LOCAL_LLAMA = True  # Set False to use OpenAI API
OPENAI_MODEL = "gpt-4"  # Set a specific OpenAI model
LLAMA_MODEL = "llama3"  # Set a specific LLaMA model
TEMPERATURE = 0.2  # Set the temperature for the models
REQUEST_TIMEOUT = 60.0  # Set the request timeout for the models
HUGGINGFACE_EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"  # Specific Hugging Face embedding model

project_root = os.path.dirname(os.path.abspath(__file__))