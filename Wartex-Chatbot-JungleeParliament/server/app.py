from flask import Flask, request, jsonify, send_from_directory  # Importing necessary libraries
from chatbot import ChatBot  # Importing the ChatBot class from chatbot.py
import os  # Importing the os module to access environment variables
from dotenv import load_dotenv  # Importing the load_dotenv function to load environment variables from .env file
from datetime import datetime, timedelta  # Importing the datetime and timedelta classes from the datetime module
import traceback  # Importing the traceback module to log error stack traces

# Initialize Flask app
app = Flask(__name__, static_folder='client/dist', static_url_path='')

# Load environment variables
load_dotenv()

# Initialize ChatBot
api_key = os.getenv('GOOGLE_API_KEY')
chatbot = ChatBot(api_key=api_key)


# Helper function to get current time
def get_time():
    current_time = datetime.now()
    if current_time.microsecond >= 500_000:
        rounded_time = current_time + timedelta(seconds=1)
    else:
        rounded_time = current_time
    return rounded_time.replace(microsecond=0)


# In-memory store for chat history (you can replace this with a file or database if needed)
chat_history_store = {}


# API endpoint to handle chat messages
@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_input = data.get("message")

    if user_input.lower() == 'exit':
        return jsonify({"response": "Goodbye!"}), 200
    elif user_input == 'history':
        return jsonify({"response": chat_history_store}), 200  # Return the chat history from the in-memory store

    try:
        response = chatbot.send_prompt(user_input)
        time = get_time()
        chat_history_store[str(time)] = {"prompt": user_input, "response": response}  # Store chat history in memory
        return jsonify({"response": response})
    except Exception as e:
        # Log the full error stack trace for debugging
        print("Error Traceback:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500  # Convert exception to string


# API endpoint to get chat history
@app.route('/api/chat_history', methods=['GET'])
def get_chat_history():
    return jsonify(chat_history_store)  # Return the in-memory chat history


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_file = os.path.join(app.static_folder, path)

    # Check if the requested path is available as a file
    if path != "" and os.path.exists(static_file):
        return send_from_directory(app.static_folder, path)
    else:
        # Log what is being served to aid debugging
        print(f"Serving index.html for path: {path}")
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
