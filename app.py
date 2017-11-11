"""
To-Do list application

Author:  Anshul Kharbanda
Created: 11 - 10 - 2017
"""
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from forms import NewToDoForm

# Create and configure app
app = Flask(__name__, template_folder='views')
app.config.from_pyfile('config.py')

# Create mongo
mongo = PyMongo(app)

def get_all_todos():
    """
    Returns the todos from the database

    :return: the todos from the database
    """
    return mongo.db.todos.find()

def create_todo(text):
    """
    Creates a new todo from the given text

    :param text: the text of the new todo
    """
    mongo.db.todos.insert_one({"text": text})

# Routes
@app.route('/')
@app.route('/index')
def index_page():
    """
    Index page of the app
    """
    return render_template(
        template_name_or_list='index.html',
        todos=get_all_todos())

@app.route('/todos/create', methods=['GET', 'POST'])
def todos_create_page():
    """
    Handles creating todos on POST.
    Returns To-Do creation page on GET
    """
    form = NewToDoForm()
    if form.validate_on_submit():
        print('Creating new TODO: {}'.format(form.text.data))
        create_todo(form.text.data)
        return redirect('/index')
    else:
        return render_template(
            template_name_or_list='create.html',
            form=form)

# Start app
if __name__ == '__main__':
    app.run(debug=True)
