from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, current_app
from flask import send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import datetime
import os

from app import db, bcrypt, base_url
from app.models import User
import utils

main = Blueprint('main', __name__)

def auto_login():
    if not current_user.is_authenticated:
        user = User.query.filter_by(username='aatalay').first()
        login_user(user, remember=True)

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    auto_login()
    script, div, cdn_js = plot()
    return render_template('home.html', script=script, div=div, cdn_js=cdn_js)

from os import listdir, remove
from os.path import isfile, isdir, splitext, abspath, join

@main.route('/uploads/<path:filename>')
def send_file(filename):
    print(filename)
    share_folder = abspath(join('.', current_app.config['SHARE_FOLDER']))
    return send_from_directory(share_folder, filename, as_attachment=True)

import re

@main.route('/uploads', methods=['GET', 'POST'])
def uploads():
    auto_login()
    share_folder = current_app.config['SHARE_FOLDER']
    regex = current_app.config['IGNORED_FILES']
    files = [f for f in listdir(share_folder) if isfile(join(share_folder, f)) and not re.match(regex, f)]
    #file_links = [f'{base_url}/uploads/{f}' for f in files]
    folders = [f for f in listdir(share_folder) if isdir(join(share_folder, f))]
    return render_template('uploads.html', title="Uploads", files=files, folders=folders)

import os
from werkzeug.utils import secure_filename
def get_filename(filename):
    share_folder = current_app.config['SHARE_FOLDER']
    regex = current_app.config['IGNORED_FILES']
    files = [f for f in listdir(share_folder) if isfile(join(share_folder, f)) and not re.match(regex, f)]
    if filename in files:
        fname, fext = splitext(filename)
        sp = fname.split('_')
        n = 0
        if len(sp) > 1:
            try:
                n = int(sp[-1]) + 1 # '0' -> 1
            except ValueError as e:
                pass
            else:
                sp = sp[:-1]
        filename = f'{"".join(sp)}_{n}{fext}'
        return get_filename(filename)
    return join(share_folder, filename)

@main.route('/upload-file', methods=['POST'])
def upload_file():
    for key in request.files.keys():
        f = request.files[key]
        filename = secure_filename(f.filename)
        filename = get_filename(filename)
        if not filename:
            return jsonify(success=False), 400
        f.save(filename)
    return jsonify(success=True), 200

@main.route('/delete-file', methods=['GET'])
def delete_file():
    cmd = dict(request.args)
    if not cmd:
        return jsonify(success=False), 400
    filename = cmd.get('filename')
    if not filename:
        return jsonify(success=False), 400
    filename = secure_filename(filename)
    share_folder = current_app.config['SHARE_FOLDER']
    try:
        remove(join(share_folder, filename))
    except FileNotFoundError as e:
        return jsonify(success=False), 400
    else:
        return jsonify(success=True), 200

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    #token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
            login_user(user, remember=True)
            return redirect(url_for('main.home'))
        flash('Invalid name or password', 'error')

    return render_template('login.html', title='Log in')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user:
            flash('Username already taken!', 'error')
        elif request.form.get('password') == request.form.get('confirm_password'):
            hashed_pw = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            user = User(username=request.form.get('username'), password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash('Created new account', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('passwords must be same', 'error')

    return render_template('signup.html', title='Sign up')


@main.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/get_temp_data', methods=['GET'])
def get_temp_data():
    return jsonify(points=utils.get_cpu_temp())

def plot():
    from bokeh.models import AjaxDataSource, CustomJS
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import components
    from bokeh.layouts import gridplot

    adapter = CustomJS(code="""
        const result = {x:[], y:[]}
        const pts = cb_data.response.points
        result.x.push(pts[0])
        result.y.push(pts[1])
        return result
        """)
    source = AjaxDataSource(data_url=f'{url_for("main.get_temp_data")}', polling_interval=500, adapter=adapter, mode='append', method='GET', max_size=10)
    ar = 16/9
    height = 300
    TOOLTIPS = [("temp", "$y"), ("time", "$x")]
    p = figure(title='rpi cpu temp', output_backend='webgl', plot_width=int(ar*height), plot_height=height, x_axis_type='datetime', tooltips=TOOLTIPS, y_range=(0, 100))
    p.line(x='x', y='y', source=source)
    p.toolbar.logo = None
    p.toolbar_location = None


    script, div = components(p)
    cdn_js = CDN.js_files
    return script, div, cdn_js
