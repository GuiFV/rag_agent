from flask import Flask, render_template, request, jsonify, session
from services import processors
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cv_generator', methods=['GET', 'POST'])
def cv_generator():
    if request.method == 'POST':
        job_description = request.form['job_description']
        return f"Job Description Received: {job_description}"

    return render_template('cv_generator.html')


@app.route('/basic_gpt', methods=['GET', 'POST'])
def basic_gpt():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']

        # Append user input to session
        session['chat_history'].append({"role": "user", "content": user_input})
        session.modified = True

        processed_input = processors.process_input(user_input, session['chat_history'])

        session['chat_history'].append({"role": "assistant", "content": processed_input})
        session.modified = True

        return render_template('basic_gpt.html', chat_history=session['chat_history'])

    return render_template('basic_gpt.html', chat_history=session['chat_history'])


@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    session.clear()
    return jsonify({"status": "Chat history reset."})


if __name__ == '__main__':
    app.run(debug=True)
