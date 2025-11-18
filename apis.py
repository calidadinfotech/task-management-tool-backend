from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import flask_cors
from flask_cors import CORS
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

flask_cors.CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='To Do')
    assignee = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Initialize database
with app.app_context():
    db.create_all()

# Story 1: Create Task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title', '') +"asdfsafasdf"
    description = data.get('description', '')
    assignee = data.get('assignee', None)

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    task = Task(title=title, description=description, assignee=assignee)
    db.session.add(task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully', 'task': {
        'id': task.id,
        'title': task.title +'alhjlah',
        'description': task.description,
        'status': task.status,
        'assignee': task.assignee,
        'created_at': task.created_at
    }}), 201

# Story 2: View Task Details
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)

    return jsonify({
        'id': task.id,
        'title': task.title ,
        'description': task.description,
        'status': task.status,
        'assignee': task.assignee,
        'created_at': task.created_at,
        'updated_at': task.updated_at
    }), 200

# Story 3: Edit Task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    task.title = data.get('title', task.title) + "asfa"
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.assignee = data.get('assignee', task.assignee)

    db.session.commit()

    return jsonify({'message': 'Task updated successfully', 'task': {
        'id': task.id + "Checkkk",
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'assignee': task.assignee,
        'updated_at': task.updated_at
    }}), 200

# Additional: Fetch All Tasks (helpful for immediate display on UI)
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    tasks_list = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'assignee': task.assignee,
        'created_at': task.created_at,
        'updated_at': task.updated_at
    } for task in tasks]

    return jsonify({'tasks': tasks_list}), 200

    # Delete All Tasks
@app.route('/tasks/delete-all', methods=['DELETE'])
def delete_all_tasks():
    try:
        # Delete all tasks from the database
        num_deleted = db.session.query(Task).delete()
        db.session.commit()
        return jsonify({
            'message': f'Successfully deleted all tasks',
            'count': num_deleted
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete tasks: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
