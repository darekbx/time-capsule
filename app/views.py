from app import app
from app.forms import LoginForm
from app import models, login_manager
from flask import g, render_template, redirect
from flask_login import current_user, login_user, logout_user, login_required
from dateutil.parser import parse

from app.dir_utils import DirUtils

import time, datetime as dt
import os
from os.path import expanduser
import hashlib

@app.route('/')
@app.route('/dir/')
@app.route('/dir/<path:dir>')
@login_required
def index(dir = ""):
	absolute_dir = app.config["RESOURCES-DIRECTORY"] + "/" + dir
	content = DirUtils().fetch_content(absolute_dir, dir, dir is "")
	return render_template('index.html', content = content)

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
