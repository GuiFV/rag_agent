from llama_index.core.agent import ReActAgent
from services.main_processors import load_llm, load_vector_store


def query_engine_loader(source_data_folder):
    llm = load_llm()

    vector_store = load_vector_store(source_data_folder)
    if vector_store is None:
        print(
            f"Error: Unable to load vector store. The persist directory '{source_data_folder}' might be empty or invalid.")
        return None

    # Create a query engine from the vector store
    query_engine = vector_store.as_query_engine(llm=llm)
    return query_engine


def agent_call(tools: list):
    llm = load_llm()
    agent = ReActAgent.from_tools(tools, llm=llm, verbose=True)
    return agent


def process_agent(primer, data_source, tools):
    response = agent_call(tools).chat(f"Consider the following: {data_source}. Now, {primer}")
    print(response)
    return response
