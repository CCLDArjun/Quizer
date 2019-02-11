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
from pygal.style import Style
import datetime
import os 
from blueprints import User, Challenge, Solved, db
from flaskext.csrf import *
import bleach

mod = Blueprint('users', __name__)

def get_graph_data(username):
	try:
		custom_style = Style(colors=("#00ff00","#ff0000"), background="transparent")
		graph = pygal.Pie(inner_radius=0.30, style=custom_style, width=500, height=400, explicit_size=True)
		user = User.query.filter_by(username=username).first()
		graph.title = "Accuracy %"
		num_tries = int(user.tries)
		num_correct = len(user.solved_challenges)
		num_incorrect = num_tries - num_correct
		graph.add("Correct", (num_correct/num_tries)*100)
		graph.add("Incorrect", (num_incorrect/num_tries)*100)
		return graph.render_data_uri()
	except ZeroDivisionError:
		return None

@mod.route("/login/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = User.query.filter_by(username=request.form['username']).first()			
		if user:
			hashed_password = user.password
			attempted_password = str(request.form['password'])
			if check_password_hash(hashed_password, attempted_password):
				session['username'] = user.username
				return redirect(url_for("main.home"))
			flash(u"Incorrect Password", at.red.value)
			return render_template("SigninOrSignup.html", type="Log In", session=session)
		flash(u"User Does Not Exist", at.red.value)
	return render_template("SigninOrSignup.html", type="Log In", session=session)

@mod.route("/signup/", methods=["GET", "POST"])
def signup():
	username = "something"
	password = "something"
	email = "something"
	if request.method == "POST":
		username = str(request.form['username'])
		email = str(request.form['email']) 
		password = generate_password_hash(str(request.form['password']), method='sha256')
		x = User.query.filter_by(username=username).first()
		y = User.query.filter_by(email=email).first()
		if x:
			flash("This username has already been taken", at.red.value)
		elif y:
			flash("User with email has already been created", at.red.value)
		else:
			new_user = User(username=bleach.clean(username), password=password, email=email, points=0)
			db.session.add(new_user)
			db.session.commit()
			session['username'] = new_user.username
			flash("New user has been created!", at.green.value)
	return render_template("SigninOrSignup.html", type="Sign Up", session=session)

@mod.route("/logout/")
def logout():
	session.pop('username', None)
	session.clear()
	return redirect(url_for("main.home"))

@mod.route('/u', defaults={'path': ''})
@mod.route('/u/<path:path>', methods=["GET", "POST"])
def catch_all_users(path):
	solved_challenges = []
	user = User.query.filter_by(username=path).first()
	if user is None:
		return abort(404)
	for challenge in user.solved_challenges:
		solved_challenges.append(challenge)
	return render_template("user_info.html", solved_challenges = solved_challenges, user = user, graph_data=get_graph_data(user.username))