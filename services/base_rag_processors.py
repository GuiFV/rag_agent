from dotenv import load_dotenv
from llama_index.core.schema import NodeWithScore

from services.main_processors import load_vector_store, get_combined_input, load_llm

load_dotenv()


def process_rag_chat(persist_directory, query_text, chat_history=None):
    # Load the vector-based index
    index = load_vector_store(persist_directory)

    if index is None:
        # Gracefully handle the case where the index couldn't be loaded
        return "Error: Unable to load the index. The persist directory is empty. Please load the required files."

    llm = load_llm()

    # Create chat engine
    chat_engine = index.as_chat_engine(llm=llm, max_iterations=5)

    # Combine chat history (if available) and the new user input
    if chat_history:
        combined_input = get_combined_input(chat_history) + f"\nuser: {query_text}"
    else:
        combined_input = f"user: {query_text}"

    # Get response from the chat engine
    response = chat_engine.chat(combined_input)

    # Handle non-serializable responses (like NodeWithScore)
    if isinstance(response, NodeWithScore):
        # Extract content and score, return in a serializable format
        return f"{response.node.get_content()} (Score: {response.score})"
    elif hasattr(response, "text"):
        # Use text attribute if it exists
        return response.text
    else:
        # Fallback to string conversion
        return str(response)
