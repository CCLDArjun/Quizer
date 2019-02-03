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
from blueprints import *

mod = Blueprint('challenges', __name__)

def sort(array_p):
	array = array_p
	less = []
	equal = []
	greater = []
	if len(array) > 1:
	    pivot = array[0].points
	    for x in array:
	        if x.points > pivot:
	            less.append(x)
	        elif x.points == pivot:
	            equal.append(x)
	        elif x.points < pivot:
	            greater.append(x)
	    return sort(less)+equal+sort(greater) 
	else:  
	    return array

def login_required(f):
	def func_wrapper(*args, **kwargs):  
		try:
			print(session['username'])
		except Exception as e:
			print(None)
		if 'username' in session:
			return f(*args, **kwargs)
		else:
			flash('Please Login First', at.red.value)
			return redirect(url_for('users.login'))
	return func_wrapper

def get_graph_data():
	custom_style = Style(background="transparent")
	graph = pygal.DateTimeLine(x_label_rotation=35, truncate_label=-1, no_data_text="", style=custom_style, width=1000, height=500, explicit_size=True)
	for x in range(1, len(User.query.all())+1):
		if Solved.query.filter_by(user_id=x).first() is None:
			continue
		data = [(User.query.filter_by(id=x).first().date_created, 0)]
		for y in range(1, len(list(Solved.query.filter_by(user_id=x)))+1):
			row = Solved.query.filter_by(user_id=x)[y-1]
			data.append((row.timestamp, float(Challenge.query.filter_by(id=row.channel_id).first().points)+float(data[y-1][1])))
		graph.add(User.query.filter_by(id=x).first().username, data)
	graph_data = graph.render_data_uri()
	return graph_data

def get_challenge_graph(name):
	try:
		custom_style = Style(colors=("#00ff00","#ff0000"), background="transparent")
		graph = pygal.Pie(inner_radius=0.30, style=custom_style, width=500, height=400, explicit_size=True)
		challenge = Challenge.query.filter_by(name=name).first()
		num_tries = int(challenge.tries)
		num_correct = challenge.solved_users.count()
		num_incorrect = num_tries - num_correct
		graph.add("Correct", (num_correct/num_tries)*100)
		graph.add("Incorrect", (num_incorrect/num_tries)*100)
		return graph.render_data_uri()
	except ZeroDivisionError:
		return None

@mod.route('/challenges', defaults={'path': ''})
@mod.route('/challenges/<path:path>', methods=["GET", "POST"])
def catch_all(path):
	challenge = Challenge.query.filter_by(id=path).first()
	if challenge is None:
		return abort(404)
	if 'username' in session:
		if challenge in User.query.filter_by(username=session['username']).first().solved_challenges:
			return render_template("answer_challenge.html", challenge=challenge, solved=True, num_solves=challenge.solved_users.count(), graph_data=get_challenge_graph(challenge.name))
		if request.method == "POST":
			print("hi")
			user=User.query.filter_by(username=session['username'])[0]
			user.tries += 1
			challenge.tries += 1
			db.session.commit()
			attempted_answer = str(request.form['answer'])
			if challenge.answer == attempted_answer:
				flash('Correct!', at.green.value)
				user.points += challenge.points
				challenge.solved_users.append(user)
				db.session.commit()
				return render_template("answer_challenge.html", challenge=challenge, solved=True, num_solves=challenge.solved_users.count(), graph_data=get_challenge_graph(challenge.name))
			else:
				flash('Incorrect', at.yellow.value)
		return render_template("answer_challenge.html", challenge=challenge, solved=False, num_solves=challenge.solved_users.count(), graph_data=get_challenge_graph(challenge.name))
	else:
		flash('You have to log in before attempting any questions', at.red.value)
		return redirect(url_for('users.login'))

@mod.route("/download/<input_id>")
@login_required
def download(input_id):
	try:
		challenge = Challenge.query.filter_by(id=input_id).first()
		if challenge:
			return send_file(challenge.attachment_filename, as_attachment=True)
		else:
			raise FileNotFoundError
	except FileNotFoundError:
		flash("no such file to download", at.red.value)
		return redirect(url_for("main.home"))

@mod.route('/scoreboard/')
def scoreboard():
	users = []
	string = ""
	for user in User.query.all():
		users.append(user)
	return render_template("scoreboard.html", users=sort(users), length=len(users), graph_data = get_graph_data(), graph_size = 1000)

@mod.route("/challenges/")
def challenges_page():
	if 'username' in session:
		solvedChallenges = []
		for challenge in Challenge.query.all():
			for user in challenge.solved_users:
				if user.username == session['username']:
					solvedChallenges.append(challenge)
					continue
		return render_template("challenges.html", challenges=Challenge.query.all(), points=User.query.filter_by(username=session['username']).first().points, solved_challenges=solvedChallenges)
	else:
		flash('You have to sign up before attempting any questions', at.red.value)
		return redirect(url_for('users.signup'))
