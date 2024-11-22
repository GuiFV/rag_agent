import os
import settings
from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage

load_dotenv()

project_root = settings.project_root

PERSIST_DIR = os.path.join(project_root, "data/cv_module/persist")

CV_SOURCE_DATA = os.path.join(project_root, "data/cv_module/source_data")


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


def process_cv():
    try:
        # load all documentos from source folder
        documents = SimpleDirectoryReader(CV_SOURCE_DATA).load_data()
        # index all documents
        index = VectorStoreIndex.from_documents(documents)
        # persist the vector database of documents as embedding on designated folder
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        message = "CV processed successfully."

    except Exception as e:
        message = f"Failed to process CVs: {str(e)}"

    return message


def add_files_to_index():
    """redundant method to add files to index for now. left here as a note"""
    # load all documentos from source folder
    documents = SimpleDirectoryReader(CV_SOURCE_DATA).load_data()
    # prepare an empty VectorStoreIndex
    index = VectorStoreIndex([])
    # add all documents again
    for doc in documents:
        index.insert(doc)


# AGENT ----------------------


def vector_loader():
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    # load index
    index = load_index_from_storage(storage_context)

    return index

query_engine = vector_loader().as_query_engine()

cv_tool = QueryEngineTool.from_defaults(
    query_engine,
    name="cv_tool",
    description="A RAG engine of the user's curriculum vitae. Collect data from the CV and ask questions about it."
)

agent = ReActAgent.from_tools([cv_tool], llm=load_llm(), verbose=True)

def process_job_description(job_description):
    primer = "compile a new CV that best matches the job description, using available tools. Do not summarize work experiences, just adapt them"
    response = agent.chat(f"Consider the following job description: {job_description}. Now, {primer}")
    print(response)
    return response