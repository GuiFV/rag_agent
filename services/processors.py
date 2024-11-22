import os
from dotenv import load_dotenv
import settings
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings as LlamaSettings
from llama_index.llms.ollama import Ollama

# Load environment variables from .env file
load_dotenv()


def get_combined_input(chat_history):
    return "\n".join([f"{message['role']}: {message['content']}" for message in chat_history])


def process_with_local_llama(input_text):
    model_name = settings.LLAMA_MODEL
    LlamaSettings.llm = Ollama(model=model_name, request_timeout=settings.REQUEST_TIMEOUT)
    response = LlamaSettings.llm.complete(input_text)
    return response


def process_with_openai_api(input_text):
    openai_api_key = os.getenv('OPENAI_API_KEY')
    model_name = settings.OPENAI_MODEL
    temperature = settings.TEMPERATURE
    openai_llm = OpenAI(api_key=openai_api_key, temperature=temperature, model=model_name)
    response = openai_llm.complete(input_text)
    return response


def process_input(input_text, chat_history):
    combined_input = get_combined_input(chat_history) + f"\nuser: {input_text}"
    if settings.USE_LOCAL_LLAMA:
        response = process_with_local_llama(combined_input)
    else:
        response = process_with_openai_api(combined_input)

    # Ensure the response is converted to a string if necessary
    if not isinstance(response, str):
        response = str(response)

    return response
