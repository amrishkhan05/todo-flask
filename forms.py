from flask_wtf import FlaskForm
from wtforms import StringField

class NewToDoForm(FlaskForm):
    """
    Form for creating new To-Do's

    Author:  Anshul Kharbanda
    Created: 11 - 10 - 2017
    """
    text = StringField('Text')
