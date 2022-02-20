"""
forms.py
-----------
Defines FlaskForms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class NewDreamForm(FlaskForm):
    title = StringField(
        '标题',
        [
            DataRequired(),
            Length(max=100, message="标题最长100字")
        ]
    )
    content = TextAreaField(
        '输入内容',
        [DataRequired()]
    )
    private = BooleanField(
        '设为私密？'
    )
    submit = SubmitField('发布梦境')
