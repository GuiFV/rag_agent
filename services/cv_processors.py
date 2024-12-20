import os

from dotenv import load_dotenv
from llama_index.core.tools import QueryEngineTool

import settings
from services.agent_processors import process_agent, query_engine_loader

load_dotenv()

project_root = settings.project_root
CV_PERSIST_DIR = os.path.join(project_root, "data/cv_module/persist")
CV_SOURCE_DATA = os.path.join(project_root, "data/cv_module/source_data")


def cv_tools():
    cv_tool = QueryEngineTool.from_defaults(
        query_engine_loader(CV_PERSIST_DIR),
        name="cv_tool",
        description="A RAG engine of the user's curriculum vitae. Collect data from the CV and ask questions about it."
    )

    return [cv_tool]


def process_cv(data_source):
    primer = "compile a new CV that best matches the job description provided, using available tools. Do not summarize work experiences, just adapt them"
    tools = cv_tools()

    reasoning_steps, final_answer, snippets = process_agent(primer, data_source, tools)
    return {
        "reasoning_steps": reasoning_steps,
        "final_answer": final_answer,
        "snippets": snippets,
    }
