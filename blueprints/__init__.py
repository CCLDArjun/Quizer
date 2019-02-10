import os
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort, send_file, send_from_directory, Blueprint
from flask_paranoid import Paranoid
from passlib.hash import sha256_crypt
from wtforms import Form, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pygal
import datetime
 

app = Flask(__name__, template_folder=os.path.abspath("templates"))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.abspath("databases/users.db"))  
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)
paranoid = Paranoid(app)
paranoid.redirect_view = '/'

class Solved(db.Model):
	__tablename__ = "solved"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	channel_id = db.Column(db.ForeignKey('challenges.id'))
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(80), unique=False, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	points = db.Column(db.Integer, unique=False, nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	tries = db.Column(db.Integer, unique=False, default=0)
	solved_challenges = db.relationship('Challenge', secondary="solved", backref=db.backref('solved_users', lazy='dynamic'))

	def __repr__(self):
		return '<User {}, {}, {}, {}, tries: {}>'.format(self.username, self.password, self.email, self.points, self.tries)

class Challenge(db.Model):
	__tablename__ = "challenges"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	points = db.Column(db.Integer, unique=False, nullable=False)
	content = db.Column(db.String(225), unique=False, nullable=False)
	answer = db.Column(db.String(225), unique=False, nullable=False)
	tries = db.Column(db.Integer, unique=False, default=0)
	attachment_filename = db.Column(db.String(255), unique=False, nullable=True)
	dynamic_point_reduction = db.Column(db.Integer, default=0)

	def __repr__(self):
		return '<Challenge {} points: {} content: {} answer: {} dynamic_point: {}>'.format(self.name, self.points, self.content[0:6], self.answer, self.dynamic_point_reduction)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html')

@app.before_request
def make_session_permanent():
    session.permanent = True

from blueprints.users.routes import mod as user
from blueprints.main.routes import mod as main
from blueprints.challenges.routes import mod as challenges
from blueprints.admin.routes import mod as admin

app.register_blueprint(user)
app.register_blueprint(challenges)
app.register_blueprint(main)
app.register_blueprint(admin, url_prefix='/admin/')



