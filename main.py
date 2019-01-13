from flask import Flask, render_template, request, url_for, redirect, session
from passlib.hash import sha256_crypt
#from MySQLdb import escape_string as thwart
#import MySQLdb
from wtforms import Form, TextField, PasswordField, validators
#from dbconnect import connection
import gc

app = Flask(__name__)


class SignupForm(Form):
	username = TextField('Username', [validators.DataRequired(), validators.Length(min=4, max=20)])
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
	return render_template("login.html")

@app.route("/signup/", methods=["GET", "POST"])
def signup():
	form = SignupForm(request.form)
	username = "something"
	password = "something"
	if request.method == "POST" and form.validate():
		username = form.username.data
		password = sha256_crypt.hash(str(form.password.data))
		print(username, password)
		return render_template("signup.html", form=form, vars=[username, password])

	return render_template("signup.html", form=form, vars=[username, password])

if __name__ == "__main__":
	app.run(debug=True)
