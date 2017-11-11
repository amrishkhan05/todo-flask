"""
To-Do list application

Author:  Anshul Kharbanda
Created: 11 - 10 - 2017
"""
from flask import Flask, render_template
from flask_pymongo import PyMongo

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

# Routes
@app.route('/')
def index():
    """
    Index page of the app
    """
    return render_template(
        template_name_or_list='index.html',
        todos=get_all_todos())

# Start app
if __name__ == '__main__':
    app.run(debug=True)
