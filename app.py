from flask import Flask, request, jsonify, g
import sqlite3
import datetime

app = Flask(__name__)
DATABASE = 'tasks.db'
API_KEY = 'your-secret-api-key'  # Change this!

# --- Database helpers ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device TEXT,
            task TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        db.commit()

# --- Authentication ---
def check_auth(request):
    key = request.headers.get('X-API-KEY')
    return key == API_KEY

# --- Routes ---
@app.route('/api/tasks', methods=['POST'])
def receive_task():
    if not check_auth(request):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    device = request.remote_addr
    task = data.get('task')
    if not task:
        return jsonify({'error': 'No task provided'}), 400

    db = get_db()
    db.execute('INSERT INTO tasks (device, task) VALUES (?, ?)', (device, task))
    db.commit()
    return jsonify({'message': 'Task received', 'task': task})

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    db = get_db()
    cur = db.execute('SELECT id, device, task, timestamp FROM tasks ORDER BY timestamp DESC LIMIT 20')
    tasks = [
        {'id': row[0], 'device': row[1], 'task': row[2], 'timestamp': row[3]}
        for row in cur.fetchall()
    ]
    return jsonify({'tasks': tasks})

# --- Main ---
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=40924)