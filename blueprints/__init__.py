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

template_dir = os.path.abspath('../templates/')
app = Flask(__name__, template_folder="/Users/arjunbemarkar/Python/Flask/CTF-Client/templates")

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format("{}{}".format(os.popen("cd ..; pwd").read()[:-1], "/databases/users.db"))
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)
paranoid = Paranoid(app)
paranoid.redirect_view = '/'

# from blueprints.utils import *
from blueprints.users.routes import mod
from blueprints.main.routes import mod
from blueprints.challenges.routes import mod

app.register_blueprint(users.routes.mod)
app.register_blueprint(challenges.routes.mod)
app.register_blueprint(main.routes.mod)



