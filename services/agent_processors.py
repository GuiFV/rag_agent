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
    query_engine = vector_store.as_query_engine(llm=llm, max_iterations=10)
    return query_engine


def agent_call(tools: list):
    llm = load_llm()
    agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, max_iterations=10)
    return agent


def process_agent(primer, data_source, tools):
    agent = agent_call(tools)
    agent_response = agent.chat(f"Consider the following: {data_source}. Now, with this user input, {primer}")

    # Access the chat history to get reasoning steps
    chat_history = agent.chat_history
    reasoning_steps = [message.content for message in chat_history if message.role == "assistant"]

    # Access source nodes for document parts used
    source_nodes = agent_response.source_nodes

    # Final response object
    final_response = agent_response.response

    # Extract text content from the nodes
    snippets = []
    for node_with_score in source_nodes:
        snippets.append(str(node_with_score.node))

    print("Reasoning Steps:")
    for step in reasoning_steps:
        print(step)

    print("Final Answer:")
    print(final_response)

    print("Sources Used:")
    for snippet in snippets:
        print(snippet)

    return reasoning_steps, final_response, snippets

