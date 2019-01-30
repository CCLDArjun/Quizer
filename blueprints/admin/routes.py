from flask import Blueprint
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort, send_file, send_from_directory
from flask_paranoid import Paranoid
from passlib.hash import sha256_crypt
from wtforms import Form, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from alert import AlertType as at
from functools import wraps
import pygal
import datetime
import os 
from blueprints import *

mod = Blueprint('admin', __name__, template_folder="admin_templates")


@mod.before_request
def check_admin():
	try:
		if session['username'] != "admin":
			abort(403)
	except KeyError:
		abort(403)

@mod.route('/')
def homepage():
	return render_template("admin_templates/index.html")

@mod.route('/add_challenge/', methods=["GET", "POST"])
def add_challenge():
	if request.method == "POST":
		name = request.form["name"]
		answer = request.form["answer"]
		points = int(request.form["points"])
		content = request.form["content"]
		for challenge in Challenge.query.all():
			if challenge.name.lower() == name.lower():
				flash("There is already a challenge with name {}".format(challenge.name), at.red.value)
				return render_template("admin_templates/add_challenge.html")			
		new_challenge = Challenge(name=name, answer=answer, points=points, content=content)
		db.session.add(new_challenge)
		db.session.commit()
	return render_template("admin_templates/add_challenge.html")










