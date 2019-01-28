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

mod = Blueprint('main', __name__)

@mod.route('/getStuff')
def getStuff():
	return 'nice'

@mod.route("/")
def home():
	print("{}".format(os.popen('pwd').read()))
	return render_template("index.html", session=session)

@mod.route("/contact/")
def contact():
	return render_template("contact.html", session=session)

@mod.route("/about/")
def about():
	return render_template("about.html", session=session)
