# Your own local RAG Agent GPT
## Interface for multiple LLM use-cases
### *Note: This project is a work in progress.*

## Features
- Local or API model execution
- RAG capabilities
- Agentic pipelines
- Llama index and Langchain usage

## Modules
- Basic GPT
- Basic RAG
- RAG Agent
- CV Generator (under development)

## How to use
### Run project
- clone and start the project under a virtual environment `python -m venv .venv`
- activate virtual env `source .venv/bin/activate` (for windows: `.\.venv\Scripts\activate`)
- install requirements `pip install -r requirements.txt`
- install Ollama `https://ollama.com/`
- rename *.env.example* to *.env* and set it up with your keys and secrets when applicable
- make necessary changes under *settings.py*
- run the app: `python app.py`
- open `http://127.0.0.1:8123`

### Documents usage
- add documents under the `data/module_name/source_data` folder for the corresponding module

### Database usage (under development)
- add SQlite3 file under `dbs` folder
- add a database url under .env file
