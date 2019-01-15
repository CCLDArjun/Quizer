from flask import Flask, render_template, request, url_for, redirect, session, flash
from passlib.hash import sha256_crypt
from wtforms import Form, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/arjunbemarkar/Python/Flask/CTF-Client/databases/users.db"
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(80), unique=True, nullable=False)

	def __repr__(self):
		return '<User {}, {}>'.format(self.username, self.password)

@app.route("/")
def home():
	return render_template("index.html", session=session)

@app.route("/contact/")
def contact():
	return render_template("contact.html", session=session)

@app.route("/about/")
def about():
	return render_template("about.html", session=session)

@app.route("/login/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = User.query.filter_by(username=request.form['username']).first()			
		if user:
			hashed_password = user.password
			attempted_password = str(request.form['password'])
			if check_password_hash(hashed_password, attempted_password):
				return redirect(url_for("home"))
			flash(u"Incorrect Password", 'danger')
			return render_template("SigninOrSignup.html", type="Log In", session=session)
		flash(u"User Does Not Exist", 'danger')
	return render_template("SigninOrSignup.html", type="Log In", session=session)

@app.route("/signup/", methods=["GET", "POST"])
def signup():
	username = "something"
	password = "something"
	if request.method == "POST":
		username = str(request.form['username'])
		password = generate_password_hash(str(request.form['password']), method='sha256')
		x = User.query.filter_by(username=username).first()
		if x:
			flash(u"This username has already been taken", 'danger')
		else:
			new_user = User(username=username, password=password)
			db.session.add(new_user)
			db.session.commit()
			session['username'] = new_user.username
			flash(u"new user has been created!", 'success')
	return render_template("SigninOrSignup.html", type="Sign Up", session=session)

@app.route("/logout/")
def logout():
	session.pop('username', None)
	return redirect(url_for("home"))

@app.route("/test/")
def test():
	if 'username' in session:
		return "Yey"
	else:
		return "<h1>you dont have access to this page</h1>"

if __name__ == "__main__":
	app.run(threaded=True)


















