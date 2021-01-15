from time import perf_counter
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for
)

app = Flask(__name__)
cluster = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
todos = cluster.todo.test


@app.route('/')
def index():
    # The main part of the Website where we be doing and handling all processes.
    saved_todos = todos.find()
    return render_template('index.html', todos=saved_todos)


@app.route('/add', methods=['POST'])
def add():
    # Add a new to-do to the DataBase.
    new_todo = request.form.get('new-todo')
    todos.insert_one({'text': new_todo, 'completed': False})
    return redirect(url_for('index'))


@app.route('/completed/<oid>')
def completed(oid):
    # Mark to-do as 'completed', I mean, False → True in the DataBase.
    todo_item = todos.find_one({'_id': ObjectId(oid)})
    todo_item['completed'] = True
    todos.save(todo_item)
    return redirect(url_for('index'))


@app.route('/delete_completed')
def delete_completed():
    # Deletes to-dos that are marked as 'True' in the DataBase.
    todos.delete_many({'completed': True})
    return redirect(url_for('index'))


@app.route('/delete_all')
def delete_all():
    # Deletes all to-dos no matter what are they, shortly, it's reset feature.
    todos.delete_many({})
    return redirect(url_for('index'))


@app.route('/latency')
def latency():
    # Check the latency of the DataBase that handles all of these todos.
    s = perf_counter()
    cluster.todo.command('ping')
    e = perf_counter()
    return f'The MongoDB latency is: {e - s:.3f} ms'


if __name__ == '__main__':
    app.run(debug=True)
