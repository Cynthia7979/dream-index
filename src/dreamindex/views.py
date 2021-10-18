"""
Sets up all routings of the application.
设置全网站的路由
"""

from dreamindex import app
from flask import render_template


@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/rand/dream')
def random_dream():
    return '<p>Hello, World!</p>'


@app.route('/rand/fanart')
def random_fanart():
    return '<p>Hello, World!</p>'


@app.route('/new/dream')
def create_dream():
    return '<p>Hello, World!</p>'


@app.route('/new/fanart')
@app.route('/new/fanart/<int:dream_id>')
def create_fanart(dream_id):
    return '<p>Hello, World!</p>'
