from flask import Flask

app = Flask(__name__)


@app.route('/')
def home_page():
    return '<p>Hello, World!</p>'


@app.route('/rand/dream')
def random_dream():
    return '<p>Hello, World!</p>'


@app.route('/rand/fanart')
def random_fanart():
    return '<p>Hello, World!</p>'
