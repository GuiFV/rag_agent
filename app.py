from flask import Flask, render_template, request, jsonify, session
from services import main_processors, cv_processors
import os

from services.setup import ensure_data_folders

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cv_generator', methods=['GET', 'POST'])
def cv_generator():
    message = None
    if request.method == 'POST':
        if 'load_cv' in request.form:
            message = cv_processors.process_file_cv()

        else:
            job_description = request.form['job_description']
            cv_processors.process_cv(data_source=job_description)
            message = f"Job Description Processed."

    return render_template('cv_generator.html', message=message)


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


@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    session.clear()
    return jsonify({"status": "Chat history reset."})


if __name__ == '__main__':
    ensure_data_folders()
    app.run(port=8123, debug=True)
