"""
forms.py
-----------
Defines FlaskForms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length


class NewDreamForm(FlaskForm):
    pass
