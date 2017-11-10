"""
To-Do list application

Author:  Anshul Kharbanda
Created: 11 - 10 - 2017
"""
from flask import Flask, render_template

# Create app
app = Flask(__name__)

# Routes
@app.route('/')
@app.route('/index.html')
def index():
    """
    Index page of the app
    """
    return render_template('index.html')

# Start app
app.run()
