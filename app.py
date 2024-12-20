import os

from flask import Flask, render_template, request, jsonify, session

from services import main_processors, cv_processors, rag_agent_processors
from services.base_rag_processors import process_rag_chat
from services.setup import ensure_data_folders

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/basic_gpt', methods=['GET', 'POST'])
def basic_gpt():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']

        # Append user input to session
        session['chat_history'].append({"role": "user", "content": user_input})
        session.modified = True

        processed_input = main_processors.process_input(user_input, session['chat_history'])

        session['chat_history'].append({"role": "assistant", "content": processed_input})
        session.modified = True

        return render_template('basic_gpt.html', chat_history=session['chat_history'])

    return render_template('basic_gpt.html', chat_history=session['chat_history'])


@app.route('/basic_rag', methods=['GET', 'POST'])
def basic_rag():
    if 'rag_chat_history' not in session:
        session['rag_chat_history'] = []

    message = None
    if request.method == 'POST':
        if 'load_files' in request.form:
            message = main_processors.documents_loader(
                source_data_path="data/base_rag_module/source_data",
                persist_directory="data/base_rag_module/persist"
            )

        elif 'user_input' in request.form:

            # Process user input as part of the chat mechanism
            user_input = request.form['user_input']

            # Append user's message to chat history
            session['rag_chat_history'].append({"role": "user", "content": user_input})
            session.modified = True

            # Process user query using RAG logic
            response_content = process_rag_chat(
                persist_directory="data/base_rag_module/persist",
                query_text=user_input,
                chat_history=session['rag_chat_history']
            )

            # Append assistant's response to chat history
            session['rag_chat_history'].append({"role": "assistant", "content": response_content})

            session.modified = True

    return render_template('basic_rag.html', chat_history=session['rag_chat_history'], message=message)


@app.route('/rag_agent', methods=['GET', 'POST'])
def rag_agent():
    message = None
    final_answer = None
    reasoning_steps = None
    snippets = None

    if request.method == 'POST':
        if 'load_files' in request.form:
            message = main_processors.documents_loader(
                source_data_path="data/rag_agent/source_data",
                persist_directory="data/rag_agent/persist"
            )

        else:
            # Handle the agent-processing request
            objective = request.form['objective']

            # Call process_rag_agent to retrieve response details
            result = rag_agent_processors.process_rag_agent(data_source=objective)

            # Extract reasoning, answer, and snippets
            reasoning_steps = result.get("reasoning_steps", [])
            final_answer = result.get("final_answer", "No final answer generated.")
            snippets = result.get("snippets", [])
            message = "Agent processed successfully."

    return render_template('rag_agent.html',
        message=message,
        reasoning_steps=reasoning_steps,
        final_answer=final_answer,
        snippets=snippets
    )


@app.route('/cv_generator', methods=['GET', 'POST'])
def cv_generator():
    message = None
    final_answer = None
    reasoning_steps = None
    snippets = None

    if request.method == 'POST':
        if 'load_cv' in request.form:
            message = main_processors.documents_loader(
                source_data_path="data/cv_module/source_data",
                persist_directory="data/cv_module/persist"
            )

        else:
            job_description = request.form['job_description']

            result = cv_processors.process_cv(data_source=job_description)

            reasoning_steps = result.get("reasoning_steps", [])
            final_answer = result.get("final_answer", "No response generated.")
            snippets = result.get("snippets", [])
            message = "CV processed successfully."

    return render_template('cv_generator.html',
        message=message,
        reasoning_steps=reasoning_steps,
        final_answer=final_answer,
        snippets=snippets
    )


@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    session.clear()
    return jsonify({"status": "Chat history reset."})


if __name__ == '__main__':
    ensure_data_folders()
    app.run(port=8123, debug=True)
