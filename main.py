from flask import Flask, render_template, request, url_for, redirect, session
from passlib.hash import sha256_crypt
from wtforms import Form, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/arjunbemarkar/Python/Flask/CTF-Client/databases/users.db"#"sqlite:///{}".format(path)
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
		attempted_username = request.form['username']
		attempted_password = request.form['password']			
		if attempted_username == "admin" and attempted_password == "password":
			session['username'] = 'admin'
			return redirect(url_for("home"))
	return render_template("SigninOrSignup.html", type="Log In", session=session)

@app.route("/signup/", methods=["GET", "POST"])
def signup():
	username = "something"
	password = "something"
	if request.method == "POST":
		username = request.form['username']
		password = sha256_crypt.hash(str(request.form['password']))
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


















