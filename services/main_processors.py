import os

from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI

import settings

load_dotenv()


def get_combined_input(chat_history):
    return "\n".join([f"{message['role']}: {message['content']}" for message in chat_history])


def load_llm():
    if settings.USE_LOCAL_LLAMA:
        model_name = settings.LLAMA_MODEL
        llm = Ollama(model=model_name, request_timeout=settings.REQUEST_TIMEOUT)
        print(f"Using Local LLaMA Model: {model_name}")
    else:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("Error: OPENAI_API_KEY not set. Cannot use OpenAI without API Key.")
        model_name = settings.OPENAI_MODEL
        temperature = settings.TEMPERATURE
        llm = OpenAI(api_key=openai_api_key, temperature=temperature, model=model_name)
        print(f"Using OpenAI Model: {model_name}")

    return llm


def load_embedding_model():
    if settings.USE_LOCAL_LLAMA:
        embed_model = HuggingFaceEmbedding(model_name=settings.HUGGINGFACE_EMBEDDING_MODEL)
        print(f"Using Local Embedding Model: {settings.HUGGINGFACE_EMBEDDING_MODEL}")
    else:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("Error: OPENAI_API_KEY not set. Cannot use OpenAI embeddings.")
        embed_model = OpenAIEmbedding(api_key=openai_api_key)
        print(f"Using OpenAI Embedding Model: {embed_model}")

    return embed_model


def documents_loader(source_data_path, persist_directory):
    """insert files into vector database persist directory."""
    _source_data = os.path.join(settings.project_root, str(source_data_path))
    _persist_dir = os.path.join(settings.project_root, str(persist_directory))

    try:
        embed_model = load_embedding_model()

        # Load all documents
        documents = SimpleDirectoryReader(_source_data).load_data()

        # Build vector store index
        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

        # Persist the index data
        index.storage_context.persist(persist_dir=_persist_dir)
        message = "Files processed successfully."

    except Exception as e:
        message = f"Failed to process files: {str(e)}"

    return message


def load_vector_store(source_data_folder):
    """Retrieves data from persist folder and loads it into a VectorStoreIndex."""
    # Check if the persist directory is empty
    if not os.listdir(source_data_folder):
        print(f"Warning: The persist directory '{source_data_folder}' is empty.")
        return None

    embed_model = load_embedding_model()

    # Rebuild the storage context
    storage_context = StorageContext.from_defaults(persist_dir=source_data_folder)

    # Load the index with explicit embedding model
    try:
        index = load_index_from_storage(storage_context, embed_model=embed_model)
        print(f"Index loaded with embedding model: {embed_model} (must be the same as used for indexing).")
    except Exception as e:
        print(f"Error: Failed to load the index from storage. Details: {str(e)}")
        return None

    return index


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
    """method to add extra files to index."""
    # load all documents from source folder
    documents = SimpleDirectoryReader(source_data_path).load_data()
    # prepare an empty VectorStoreIndex
    index = VectorStoreIndex([])
    # add all documents again
    for doc in documents:
        index.insert(doc)

