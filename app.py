"""
To-Do list application

Author:  Anshul Kharbanda
Created: 11 - 10 - 2017
"""
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import ToDoForm

# Create and configure app
app = Flask(__name__, template_folder='views')
app.config.from_pyfile('config.py')

# Create mongo
mongo = PyMongo(app)

def index_todos():
    """
    Returns the todos from the database

    :return: the todos from the database
    """
    return mongo.db.todos.find()

def get_todo(id):
    """
    Returns the todo with the given id

    :param id: the id of the todo

    :return: the todo with the given id
    """
    return mongo.db.todos.find_one(filter={ '_id': ObjectId(id) })

def create_todo(text):
    """
    Creates a new todo from the given text

    :param text: the text of the new todo
    """
    mongo.db.todos.insert_one(document={ 'text': text })

def update_todo(id, text):
    """
    Updates the todo with the given id to the given text

    :param id: the id of the todo
    :param text: the new text of the todo
    """
    mongo.db.todos.update_one(
        filter={ '_id': ObjectId(id) },
        update={ '$set': { 'text': text } })

def delete_todo(id):
    """
    Deletes the todo with the given id

    :param id: the id to delete
    """
    mongo.db.todos.delete_one({ '_id': ObjectId(id) })

# Routes
@app.route('/')
def todos_index_page():
    """
    Index page of the app
    """
    return render_template(
        template_name_or_list='index.html',
        todos=index_todos())

@app.route('/todos/create', methods=['GET', 'POST'])
def todos_create_page():
    """
    Handles creating todos on POST.
    Returns To-Do creation page on GET
    """
    form = ToDoForm()
    if form.validate_on_submit():
        print('Creating new TODO: {}'.format(form.text.data))
        create_todo(form.text.data)
        return redirect('/')
    else:
        return render_template(
            template_name_or_list='todo.html',
            form=form,
            handle='Create')

@app.route('/todos/<id>/edit', methods=['GET', 'POST'])
def todos_edit_page(id):
    """
    Handles Editing Todos
    """
    form = ToDoForm()
    todo = get_todo(id)
    if form.validate_on_submit():
        print('Updating TODO {id} to {text}'.format(
            id=todo['_id'],
            text=form.text.data
        ))
        update_todo(id, form.text.data)
        return redirect('/')
    else:
        return render_template(
            template_name_or_list='todo.html',
            form=form,
            todo=todo,
            handle='Edit')

@app.route('/todos/<id>/delete')
def todos_delete_function(id):
    """
    Handles deleting todos
    """
    print('Deleting TODO {id}'.format(id=id))
    delete_todo(id)
    return redirect('/')

# Start app
if __name__ == '__main__':
    app.run(debug=True)
