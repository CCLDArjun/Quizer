from flask import Blueprint
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort, send_file, send_from_directory
from flask_paranoid import Paranoid
from passlib.hash import sha256_crypt
from wtforms import Form, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import secure_filename
from alert import AlertType as at
from functools import wraps
import pygal
from pygal.style import Style
import datetime
import os 
from blueprints import *
from blueprints.utils import ChallengeAttempt

mod = Blueprint('admin', __name__, template_folder="admin_templates")

def get_people_graph():
	custom_style = Style(background="transparent")
	graph = pygal.Line(x_label_rotation=35, truncate_label=-1, no_data_text="", style=custom_style, width=1000, height=400, explicit_size=True)
	x_labels = []
	data = []
	for i in range(1,len(User.query.all())+1):
		data.append(i)
		x_labels.append(User.query.filter_by(id=i).first().date_created)
	graph.x_labels = x_labels
	graph.add("Count", data)
	graph_data = graph.render_data_uri()
	return graph_data

@mod.before_request
def check_admin():
	try:
		if session['username'] != "admin":
			abort(403)
	except KeyError:
		abort(403)

@mod.route('/')
def homepage():
	custom_style = Style(background="transparent", min_scale=1)
	graph = pygal.Bar(style=custom_style, width=700, height=200, explicit_size=True)
	num_tries = 0
	num_solves = 0
	for challenge in Challenge.query.all():
		num_tries += challenge.tries
		num_solves += challenge.solved_users.count()
		if challenge.solved_users.count() == 0:
			continue
		graph.add(challenge.name, [challenge.solved_users.count()])
	graph_data = graph.render_data_uri()
	return render_template("admin_templates/index.html", graph_data=graph_data, num_users=len(User.query.all()), num_challenges=len(Challenge.query.all()), num_solves=float(num_solves), num_tries=float(num_tries), people_overtime_graph=get_people_graph())

@mod.route("/submissions/")
def submissions():
	return render_template("admin_templates/admin_submissions.html", submissions=ChallengeAttempt.get_submissions())

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
		file=request.files["file"]
		download_filepath = None
		if 'file' in request.files:
			file = request.files["file"]
			if file and file.filename != " ":
				extension = os.path.splitext(file.filename)[1]
				file.save(os.path.join(os.path.abspath("downloadables"), name+extension))
				download_filepath = os.path.join(os.path.abspath("downloadables"), name+extension)
		new_challenge = Challenge(name=name, answer=answer, points=points, content=content, attachment_filename=download_filepath)
		db.session.add(new_challenge)
		db.session.commit()
		flash("Created New Challenge", at.green.value)
	return render_template("admin_templates/add_challenge.html")

@mod.route('/edit_challenge', defaults={'path': ''})
@mod.route('/edit_challenge/<path:path>', methods=["GET", "POST"])
def edit_challenge(path):
	challenge = Challenge.query.filter_by(id=path).first()
	if challenge is None:
		return abort(404)
	if request.method == "POST":
		if request.form["name"] != challenge.name:
			if Challenge.query.filter_by(name=request.form["name"]) is not None:
				flash("There is already a challenge with name {}".format(challenge.name), at.red.value)
				return render_template("admin_templates/add_challenge.html", type="edit", challenge=challenge)
		if 'file' in request.files:
			file = request.files["file"]
			if file and file.filename != " ":
				if challenge.attachment_filename is not None:
					os.system("sudo rm -rf {}".format(challenge.attachment_filename))
				extension = os.path.splitext(file.filename)[1]
				file.save(os.path.join(os.path.abspath("downloadables"), request.form["name"]+extension))
				challenge.attachment_filename = os.path.join(os.path.abspath("downloadables"), request.form["name"]+extension)
		challenge.name = request.form["name"]
		challenge.answer = request.form["answer"]
		challenge.points = int(request.form["points"])
		challenge.content = request.form["content"]
		db.session.commit()
		flash("successfully edited challenge", at.green.value)
	return render_template("admin_templates/add_challenge.html", type="edit", challenge=challenge)








