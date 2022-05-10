"""
forms.py
-----------
Defines FlaskForms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.widgets import PasswordInput
from dreamindex.form_validators import *


class NewDreamForm(FlaskForm):
    title = StringField('标题',
        validators=[
            InputRequired(),
            Length(max=100, message="标题最长100字")
    ])
    content = TextAreaField('输入内容', validators=[InputRequired()])
    private = BooleanField('设为私密？')
    submit = SubmitField('发布梦境')


class SignupForm(FlaskForm):
    username = StringField('用户名',
        validators=[
            InputRequired(),
            Length(max=30),
            UserNotExists(data_type='username', message='用户名已被占用')
    ])
    email = StringField('邮箱',
        validators=[
            InputRequired(),
            Email()
    ])
    password = PasswordField('密码',
        validators=[
            InputRequired(),
            StrongPassword(message="密码长度必须大于6位，且包含至少一个字母和一个数字")
        ]
    )
    password_confirm = PasswordField('重复密码',
        validators=[
            InputRequired(),
            EqualTo('password', message='两次输入的密码不相同')
        ]
    )
    terms_agreement = BooleanField('我已阅读并同意遵守')
    submit = SubmitField()