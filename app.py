from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = {
        "id": len(tasks) + 1,
        "task": data.get('task', 'unnamed'),
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
    tasks.append(task)
    return jsonify({"status": "ok", "task": task}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
