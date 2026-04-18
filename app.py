from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import urllib.request
import threading
import sqlite3

# Use absolute path to avoid path confusion when Flask reloader restarts
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ethos_users.db')

def get_db():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        import psycopg2
        # Ensure SSL is enabled for Supabase pooler connections
        if "sslmode" not in database_url:
            database_url += "?sslmode=require"
        return psycopg2.connect(database_url)
    else:
        conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA busy_timeout=30000')
        return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    if os.environ.get("DATABASE_URL"):
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id SERIAL PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT)''')
    else:
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

# Init DB on startup — wrapped in try/except so a bad DB URL never crashes the server
try:
    init_db()
except Exception as e:
    print(f"[WARNING] Database init failed: {e}. App will still start.")

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
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    try:
        conn = get_db()
        c = conn.cursor()
        param = "%s" if os.environ.get("DATABASE_URL") else "?"
        c.execute(f"INSERT INTO users (name, email, password) VALUES ({param}, {param}, {param})", (name, email, password))
        conn.commit()
        conn.close()
        return jsonify({"success": "Profile created successfully!"})
    except Exception as e:
        if "UNIQUE" in str(e) or "unique" in str(e).lower():
            return jsonify({"error": "User with this email already exists"}), 400
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    conn = get_db()
    c = conn.cursor()
    param = "%s" if os.environ.get("DATABASE_URL") else "?"
    c.execute(f"SELECT * FROM users WHERE email={param} AND password={param}", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"success": "Login successful!"})
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/view-db')
def view_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, name, email FROM users")
    users = c.fetchall()
    conn.close()
    
    html = "<h2>Registered Users Database</h2><table border='1' cellpadding='10'><tr><th>ID</th><th>Name</th><th>Email</th></tr>"
    for u in users:
        html += f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td></tr>"
    html += "</table><br><a href='/'>Back to Home</a>"
    return html

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
            # Pass the absolute path to the agent instead of reading the content
            # This allows CSVSearchTool to index the file directly
            user_data = os.path.abspath(user_input)
            print(f"Detected local file path, passing to agent: {user_data}")

    try:
        from router import determine_intent, get_general_response
        from mains import run_phase1, run_phase2
        
        intent = determine_intent(user_input, has_file=bool(file))
        
        if intent == "GENERAL":
            response_text = get_general_response(user_input)
            return jsonify({"response": response_text})
            
        elif intent == "PHASE_1":
            result = run_phase1(user_data)
            append_text = "\n\n> **Note:** Please review the CSV data above. If you approve, simply type **'Update the model'** to apply these fixes."
            return jsonify({"response": str(result) + append_text})
            
        elif intent == "PHASE_2":
            result = run_phase2(user_data)
            append_text = "\n\n> **Note:** The **Model Resolution Log** has been generated. You can view the technical 'Before vs After' comparison sheet above."
            return jsonify({"response": str(result) + append_text})
            
        else:
            return jsonify({"error": "Failed to determine intent."}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting EthosAI Chatbot Server on port {port}")
    # use_reloader=False prevents the double-process issue that causes DB lock on startup
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
