import os

from llama_index.core.tools import QueryEngineTool
from llama_index.tools.google import GoogleSearchToolSpec

import settings
from services.agent_processors import process_agent, query_engine_loader

project_root = settings.project_root
CV_PERSIST_DIR = os.path.join(project_root, "data/rag_agent/persist")
CV_SOURCE_DATA = os.path.join(project_root, "data/rag_agent/source_data")


def rag_agent_tools():
    files_tool = QueryEngineTool.from_defaults(
        query_engine_loader(CV_PERSIST_DIR),
        name="files_tool",
        description="A RAG engine tool containing the user's personal files."
    )

    google_spec = GoogleSearchToolSpec(key=settings.GOOGLE_SEARCH_API_KEY, engine=settings.GOOGLE_ENGINE)
    google_tool = google_spec.to_tool_list()
    return [files_tool] + google_tool


    # todo: wolframalpha_tool - https://llamahub.ai/l/tools/llama-index-tools-wolfram-alpha?from=



def process_rag_agent(data_source):
    primer = "reason the user's query utilizing all tools available, delivering a high quality final answer."
    tools = rag_agent_tools()

    reasoning_steps, final_answer, snippets = process_agent(primer, data_source, tools)

    return {
        "reasoning_steps": reasoning_steps,
        "final_answer": final_answer,
        "snippets": snippets
    }
