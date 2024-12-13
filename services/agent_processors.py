from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.agent import ReActAgent

from services.main_processors import load_llm


def vector_loader(source_data_folder):
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=source_data_folder)
    # load index
    index = load_index_from_storage(storage_context)
    return index


def query_engine_loader(source_data_folder):
    query_engine = vector_loader(source_data_folder).as_query_engine()
    return query_engine


def agent_call(tools: list):
    agent = ReActAgent.from_tools(tools, llm=load_llm(), verbose=True)
    return agent


def process_agent(primer, data_source, tools):
    response = agent_call(tools).chat(f"Consider the following data source: {data_source}. Now, {primer}")
    print(response)
    return response
