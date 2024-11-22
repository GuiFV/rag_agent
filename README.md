# Interface with Langchain and LLama index for multiple use-cases

## Features
- Local execution
- RAG capabilities
- Agentic pipelines

## Modules
- Basic GPT
- CV Generator

## How to use
- install Ollama
- get an openai api key if you are not using local models
- set secrets under OPENAI_API_KEY and LLAMA_CLOUD_API_KEY in a .env file on the root folder
- make necessary changes under settings.py
- under root folder, copy the following structure:
```
├── data
│   └── cv_module
│       ├── output
│       └── source_data
├── dbs
```
- add documents under any `source` folder
- add SQlite3 file under `dbs` folder





