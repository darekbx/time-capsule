from app import app
from app.forms import LoginForm, UploadForm
from app import models, login_manager
from flask import g, request, url_for, send_file, render_template, redirect, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from dateutil.parser import parse

from app.dir_utils import DirUtils

import time, datetime as dt
import os
import json
import hashlib

@app.route('/open', methods=['GET', 'POST'])
def open():
	if request.method == 'POST':
		dirUtils = DirUtils()
		path = app.config["RESOURCES-DIRECTORY"] + "/" + request.form['path']

		if dirUtils.is_SQLite3(path):
			return json.dumps({"type":"sqlite"})

		if dirUtils.is_image(path):
			return json.dumps({"type":"image","path":"file:///" + path})

		contents, error = DirUtils().read_file_contents(path)
		if contents is None:
			return error, 400
		else:
			return json.dumps({"type":"text", "content":contents.decode()})
		
	return redirect("/")

@app.route('/backup', methods=['GET', 'POST'])
def backup():
	if request.method == 'POST':
		return DirUtils().make_backup(app.config["RESOURCES-DIRECTORY"])
	return redirect("/")

@app.route('/delete', methods=['GET', 'POST'])
def delete():
	if request.method == 'POST':
		path = app.config["RESOURCES-DIRECTORY"] + "/" + request.form['path']
		DirUtils().delete_file(path)
	return redirect("/")

@app.route('/download/<path:dir>')
def download(dir):
	absolute_dir = app.config["RESOURCES-DIRECTORY"] + "/" + dir
	return send_file(absolute_dir, as_attachment=True)

@app.route('/new-dir', methods=['GET', 'POST'])
def new_dir():
	if request.method == 'POST':
		dir = request.form['dir'].replace("dir/", "")
		absolute_dir = app.config["RESOURCES-DIRECTORY"] + dir
		DirUtils().make_dir(absolute_dir, request.form['name'])
		return redirect(url_for('new_dir'))
	return redirect("/")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		form = UploadForm()
		if not form.validate_on_submit():
			flash('No file was selected')
			return redirect(request.url)

		file = request.files['file']
		dir = request.form['dir']
		request_dir = request.form['url']
		request_dir = request_dir.replace("/dir", "")
		file_to_save = DirUtils().obtain_file_to_save(dir, file.filename)
		
		file.save(file_to_save)
		return redirect(url_for("index", dir=request_dir))
	return redirect("/")

@app.route('/')
@app.route('/dir/')
@app.route('/dir/<path:dir>')
@login_required
def index(dir = ""):
	dir_utils = DirUtils()
	absolute_dir = app.config["RESOURCES-DIRECTORY"] + "/" + dir
	content = dir_utils.fetch_content(absolute_dir, dir, dir is "")
	dir_size = dir_utils.dir_size(absolute_dir)
	return render_template('index.html', 
		content = content, 
		dir_size = dir_utils.sizeof_fmt(dir_size),
		dir = absolute_dir,
		upload_form = UploadForm()
	)

@login_manager.user_loader
def load_user(user_id):
	return models.User()

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route('/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect("/")
	else:
		form = LoginForm()
		if form.validate_on_submit():
			login_user(models.User())
			return redirect("/")
		else:
			return render_template('login.html', form=form)
