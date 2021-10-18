"""
Sets up all routings of the application.
设置全网站的路由
"""

from dreamindex import app, db
from flask import render_template


@app.route('/')
def home_page():
    home_page_displays = {
        "dream_trending": db.get_dreams(),
        "dream_new": db.get_dreams(),
        "fanart_trending": db.get_fanarts(),
        "fanart_new": db.get_fanarts()
    }
    return render_template('home_page.html', home_page_displays=home_page_displays)


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
