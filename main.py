from flask import Flask, render_template, request, url_for, redirect, session
from passlib.hash import sha256_crypt
#from MySQLdb import escape_string as thwart
#import MySQLdb
from wtforms import Form, TextField, PasswordField, validators
#from dbconnect import connection
import gc

app = Flask(__name__)


class SignupForm(Form):
	username = TextField("Username", [validators.DataRequired(), validators.Length(min=4, max=20)])
	password = PasswordField("Password", [validators.DataRequired()])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact/")
def contact():
	return render_template("contact.html")

@app.route("/about/")
def about():
	return render_template("about.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		attempted_username = request.form['username']
		attempted_password = request.form['password']			
		if attempted_username == "admin" and attempted_password == "password":
			return redirect(url_for("home"))
	return render_template("LogOrSignIn.html", type="Log In")

@app.route("/signup/", methods=["GET", "POST"])
def signup():
	username = "something"
	password = "something"
	if request.method == "POST":
		username = request.form['username']
		password = sha256_crypt.hash(str(request.form['password']))
		print(username, password)
	return render_template("LogOrSignIn.html", type="Sign Up")

if __name__ == "__main__":
	app.run(debug=True)
