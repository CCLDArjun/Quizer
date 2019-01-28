from flask import Blueprint
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort, send_file, send_from_directory
from flask_paranoid import Paranoid
from passlib.hash import sha256_crypt
from wtforms import Form, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pygal
import datetime
import os 
from blueprints.__init__ import db

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
	password = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	points = db.Column(db.Integer, unique=True, nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	solved_challenges = db.relationship('Challenge', secondary="solved", backref=db.backref('solved_users', lazy='dynamic'))

	def __repr__(self):
		return '<User {}, {}, {}, {}>'.format(self.username, self.password, self.email, self.points)

class Challenge(db.Model):
	__tablename__ = "challenges"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	points = db.Column(db.Integer, unique=True, nullable=False)
	content = db.Column(db.String(225), unique=True, nullable=False)
	answer = db.Column(db.String(225), unique=True, nullable=False)

	def __repr__(self):
		return '<Challenge {} points: {} content: {} answer: {}>'.format(self.name, self.points, self.content[0:6], self.answer)