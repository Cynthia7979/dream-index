"""
Set up routings for the application.
设置全网站的路由
"""

from dreamindex import app, db
import dreamindex.cookies as cookies
import dreamindex.forms as forms
from flask import render_template, redirect, request, abort, url_for, make_response


@app.route('/')
def home_page():
    user = cookies.get_login_user()
    home_page_displays = {
        "dream_trending": db.get_dreams(sort="NumberOfLikes", count=4),
        "dream_new": db.get_dreams(sort="PublishTime", count=4),
        "fan_art_trending": db.get_fan_arts(sort="NumberOfLikes", count=4),
        "fan_art_new": db.get_fan_arts(sort="PublishTime", count=4)
    }

    return render_template('home_page.html', home_page_displays=home_page_displays, user=user)


@app.route('/rand/dream/')
def random_dream():
    random_dream_id = db.get_dreams(sort="RANDOM()", count=1)[0].id
    redirect(url_for(f'/dream/{random_dream_id}'))


@app.route('/rand/fan-art/')
def random_fan_art():
    random_fan_art_id = db.get_fan_arts(sort="RANDOM()", count=1)[0].id
    redirect(url_for(f'/dream/{random_fan_art_id}'))


@app.route('/new/dream/', methods=['GET', 'POST'])
def new_dream():
    if request.method == 'GET':
        user = cookies.get_login_user()
        form = forms.NewDreamForm()
        return render_template('new_dream.html', user=user, form=form)


@app.route('/new/fan-art/', methods=['GET', 'POST'])
@app.route('/new/fan-art/<int:dream_id>', methods=['GET'])
def new_fan_art(dream_id):
    if request.method == 'GET':
        user = cookies.get_login_user()
        return render_template('new_fanart.html', user=user)


@app.route('/dream/<int:dream_id>')
def read_dream(dream_id):
    if db.dream_exists(dream_id):
        return render_template('read_dream.html')  # TODO
    else:
        abort(404)


@app.route('/fan-art/<int:fan_art_id>')
def read_fan_art(fan_art_id):
    if db.fan_art_exists(fan_art_id):
        return render_template('read_fan_art.html')  # TODO
    else:
        abort(404)

# Account-Related 账号相关

@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
