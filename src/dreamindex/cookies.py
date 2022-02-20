"""
cookies.py
-------------
Functions that either queries or writes into cookies.
"""

from dreamindex import app, db
from flask import request


def get_login_user():
    user_id = request.cookies.get('user_id')
    if user_id == None:
        return None
    else:
        return db.get_user(user_id=user_id)
