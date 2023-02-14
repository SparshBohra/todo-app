# Importing libraries
from flask import Flask, request, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
Session(app)

# Construct the database 
class TodoItem(db.Model):
    # Auto generated
    id = db.Column(db.Integer, primary_key=True)
    # Title of item
    title = db.Column(db.String(100))
    # Status of item
    completed = db.Column(db.Boolean)

# Create the database
with app.app_context():
    db.create_all()

    # db.session.add(TodoItem('Do homework', False))
    # db.session.add(TodoItem('Go out', False))
    # db.session.commit()

    # todos = TodoItem.query.all()
    # print(todos)

@app.route('/')
def home():
    return "Todo List app!"

# Returns all the items in the todo list
@app.route('/api/todo')
def get_todo_list():
    todo_items = TodoItem.query.all()
    items = [{'id': item.id, 'title': item.title, 'completed': item.completed} for item in todo_items]
    return jsonify(items)

# Adds item to the list with default status incomplete
@app.route('/api/todo', methods=['POST'])
def add_todo_item():
    title = request.json.get('title')
    print(title)
    if not title:
        return jsonify({'success': False, 'message': 'Title is required.'})
    item = TodoItem(title=title, completed=False)
    db.session.add(item)
    db.session.commit()
    return jsonify({'success': True})

# Updates completion status of item
@app.route('/api/todo/<int:id>/complete', methods=['POST'])
def complete_todo_item(id):
    item = TodoItem.query.get(id)
    if not item:
        return jsonify({'success': False, 'message': 'Item not found.'})
    item.completed = True
    db.session.commit()
    return jsonify({'success': True})

# PUT method for editing item title
@app.route('/api/todo/<int:id>', methods=['PUT'])
def update_todo_item(id):
    item = TodoItem.query.get(id)
    if not item:
        return jsonify({'success': False, 'message': 'Item not found.'})
    title = request.json.get('title')
    if not title:
        return jsonify({'success': False, 'message': 'Title is required.'})
    item.title = title
    db.session.commit()
    return jsonify({'success': True})

# DELETE method for deleting item
@app.route('/api/todo/<int:id>', methods=['DELETE'])
def delete_todo_item(id):
    item = TodoItem.query.get(id)
    if not item:
        return jsonify({'success': False, 'message': 'Item not found.'})
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)