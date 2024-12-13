import os
import settings
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

load_dotenv()


def get_combined_input(chat_history):
    return "\n".join([f"{message['role']}: {message['content']}" for message in chat_history])


def load_llm():
    if settings.USE_LOCAL_LLAMA:
        model_name = settings.LLAMA_MODEL
        llm = Ollama(model=model_name, request_timeout=settings.REQUEST_TIMEOUT)
    else:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        model_name = settings.OPENAI_MODEL
        temperature = settings.TEMPERATURE
        llm = OpenAI(api_key=openai_api_key, temperature=temperature, model=model_name)

    return llm


def process_message(input_text):
    llm = load_llm()
    response = llm.complete(input_text)
    return response


def process_input(input_text, chat_history):
    combined_input = get_combined_input(chat_history) + f"\nuser: {input_text}"
    response = process_message(combined_input)

    if not isinstance(response, str):
        response = str(response)

    return response


def add_files_to_index(source_data_path):
    """method to add files to index."""
    # load all documents from source folder
    documents = SimpleDirectoryReader(source_data_path).load_data()
    # prepare an empty VectorStoreIndex
    index = VectorStoreIndex([])
    # add all documents again
    for doc in documents:
        index.insert(doc)

