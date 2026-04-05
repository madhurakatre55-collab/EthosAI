from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from mains import Ethos_crew
import os
import urllib.request
import threading
import sqlite3

def init_db():
    conn = sqlite3.connect('ethos_users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__, static_folder='frontend')
CORS(app)

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat')
def serve_chat():
    return send_from_directory(app.static_folder, 'chat.html')

@app.route('/login')
def serve_login():
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    try:
        conn = sqlite3.connect('ethos_users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()
        return jsonify({"success": "Profile created successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "User with this email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect('ethos_users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"success": "Login successful!"})
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message', '').strip()
    file = request.files.get('file')
    
    if not user_input and not file:
        return jsonify({"error": "Empty message and no file attached"}), 400

    user_data = user_input
    
    if file:
        try:
            file_content = file.read().decode('utf-8')
            user_data = f"Attached File Data:\n{file_content}\n\nUser Instructions:\n{user_input}"
        except Exception as e:
            return jsonify({"error": f"Failed to read attached file: {str(e)}"}), 400
    else:
        # Handle URLs (like mains.py does)
        if user_input.startswith("http://") or user_input.startswith("https://"):
            try:
                response = urllib.request.urlopen(user_input)
                user_data = response.read().decode('utf-8')
            except Exception:
                pass # Keep original
        
        # Check if local path
        elif os.path.exists(user_input) and os.path.isfile(user_input):
            try:
                with open(user_input, 'r', encoding='utf-8') as f:
                    user_data = f.read()
            except:
                pass # Keep original

    try:
        # Kick off the EthosAI crew
        result = Ethos_crew.kickoff(inputs={"user_data": user_data})
        return jsonify({"response": result.raw})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("starting EthosAI Chatbot Server on http://localhost:5000")
    app.run(debug=True, port=5000)
