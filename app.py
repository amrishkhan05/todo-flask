"""
To-Do list application

Author:  Anshul Kharbanda
Created: 11 - 10 - 2017
"""
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from models import Todo

# Create and configure app, get database
app = Flask(__name__, template_folder='views')
app.config.from_pyfile('config.py')
mongo = PyMongo(app)

# Routes
@app.route('/')
def todos_index_page():
    """
    Index page of the app
    """
    return render_template(
        template_name_or_list='index.html',
        todos=Todo.index(mongo.db))

@app.route('/todos/create', methods=['GET', 'POST'])
def todos_create_page():
    """
    Handles creating todos on POST.
    Returns To-Do creation page on GET
    """
    todo = Todo()
    if todo.form.validate_on_submit():
        todo.update(mongo.db)
        print('Created new TODO: {text}'.format(**todo.doc))
        return redirect('/')
    else:
        return render_template(
            template_name_or_list='todo.html',
            todo=todo,
            handle='Create')

@app.route('/todos/<id>/edit', methods=['GET', 'POST'])
def todos_edit_page(id):
    """
    Handles Editing Todos
    """
    todo = Todo.get(mongo.db, id)
    if todo.form.validate_on_submit():
        todo.update(mongo.db)
        print('Updated TODO {_id} to {text}'.format(**todo.doc))
        return redirect('/')
    else:
        return render_template(
            template_name_or_list='todo.html',
            todo=todo,
            handle='Edit')

@app.route('/todos/<id>/delete')
def todos_delete_function(id):
    """
    Handles deleting todos
    """
    todo = Todo.get(mongo.db, id)
    todo.delete(mongo.db)
    print('Deleted TODO {_id}'.format(**todo.doc))
    return redirect('/')

# Start app
if __name__ == '__main__':
    app.run(debug=True)
