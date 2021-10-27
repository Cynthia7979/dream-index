"""
Sets up all routings of the application.
设置全网站的路由
"""

from dreamindex import app, db
from flask import render_template


@app.route('/')
def home_page():
    home_page_displays = {
        "dream_trending": db.get_dreams(sort="NumberOfLikes", count=4),
        "dream_new": db.get_dreams(sort="PublishTime", count=4),
        "fan_art_trending": db.get_fan_arts(sort="NumberOfLikes", count=4),
        "fan_art_new": db.get_fan_arts(sort="PublishTime", count=4)
    }

    return render_template('home_page.html', home_page_displays=home_page_displays)


@app.route('/rand/dream/')
def random_dream():
    return '<p>Hello, World!</p>'


@app.route('/rand/fan-art/')
def random_fan_art():
    return '<p>Hello, World!</p>'


@app.route('/new/dream/')
def create_dream():
    return '<p>Hello, World!</p>'


@app.route('/new/fan-art/')
@app.route('/new/fan-art/<int:dream_id>')
def create_fan_art(dream_id):
    return '<p>Hello, World!</p>'


@app.route('/dream/<int:dream_id>')
def read_dream(dream_id):
    return '<p>Hello, World!</p>'


@app.route('/fan-art/<int:fan_art_id>')
def read_fan_art(fan_art_id):
    return '<p>Hello, World!</p>'
