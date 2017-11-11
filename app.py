"""
To-Do list application

Author:  Anshul Kharbanda
Created: 11 - 10 - 2017
"""
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from models import Todo, ToDoForm

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
    form = ToDoForm()
    if form.validate_on_submit():
        print('Creating new TODO: {}'.format(form.text.data))
        Todo(text=form.text.data).save(mongo.db)
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
    todo = Todo.get(mongo.db, id)
    if form.validate_on_submit():
        print('Updating TODO {id} to {text}'.format(id=todo._id, text=todo.text))
        todo.text = form.text.data
        todo.save(mongo.db)
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
    Todo.get(mongo.db, id).delete(mongo.db)
    return redirect('/')

# Start app
if __name__ == '__main__':
    app.run(debug=True)
