from flask import Flask, render_template, request, url_for, redirect, session, flash, abort
from passlib.hash import sha256_crypt
from wtforms import Form, TextField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from alert import AlertType as at
import pygal
import datetime
import os 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format("{}{}".format(os.popen("pwd").read()[:-1], "/databases/users.db"))
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)

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

@app.route("/")
def home():
	return render_template("index.html", session=session)

@app.route("/contact/")
def contact():
	return render_template("contact.html", session=session)

@app.route("/about/")
def about():
	return render_template("about.html", session=session)

def get_graph_data():
	graph = pygal.DateTimeLine(x_label_rotation=35, truncate_label=-1)
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

@app.route("/login/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = User.query.filter_by(username=request.form['username']).first()			
		if user:
			hashed_password = user.password
			attempted_password = str(request.form['password'])
			if check_password_hash(hashed_password, attempted_password):
				session['username'] = user.username
				return redirect(url_for("home"))
			flash(u"Incorrect Password", at.red.value)
			return render_template("SigninOrSignup.html", type="Log In", session=session)
		flash(u"User Does Not Exist", at.red.value)
	return render_template("SigninOrSignup.html", type="Log In", session=session)

@app.route("/signup/", methods=["GET", "POST"])
def signup():
	username = "something"
	password = "something"
	email = "something"
	if request.method == "POST":
		username = str(request.form['username'])
		email = str(request.form['email'])
		password = generate_password_hash(str(request.form['password']), method='sha256')
		x = User.query.filter_by(username=username).first()
		y = User.query.filter_by(email=email).first()
		if x:
			flash("This username has already been taken", at.red.value)
		elif y:
			flash("User with email has already been created", at.red.value)
		else:
			new_user = User(username=username, password=password, email=email, points=0)
			db.session.add(new_user)
			db.session.commit()
			session['username'] = new_user.username
			flash("New user has been created!", at.green.value)
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
		return "<h1>you dont have access to this page, {}</h1>".format(session)

@app.route("/challenges/")
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
		return redirect(url_for('signup'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/scoreboard/')
def scoreboard():
	users = []
	string = ""
	for user in User.query.all():
		users.append(user)
	return render_template("scoreboard.html", users=sort(users), length=len(users), graph_data = get_graph_data(), graph_size = 1000)

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

@app.route('/challenges', defaults={'path': ''})
@app.route('/challenges/<path:path>', methods=["GET", "POST"])
def catch_all(path):
	challenge = Challenge.query.filter_by(name=path).first()
	if challenge is None:
		return abort(404)
	if 'username' in session:
		if challenge in User.query.filter_by(username=session['username']).first().solved_challenges:
			return render_template("answer_challenge.html", challenge=challenge, solved=True)
		if request.method == "POST":
			attempted_answer = str(request.form['answer'])
			if challenge.answer == attempted_answer:
				flash('Correct!', at.green.value)
				user=User.query.filter_by(username=session['username'])[0]
				user.points += challenge.points
				challenge.solved_users.append(user)
				db.session.commit()
				return render_template("answer_challenge.html", challenge=challenge, solved=True)
			else:
				flash('Incorrect', at.yellow.value)
		return render_template("answer_challenge.html", challenge=challenge, solved=False)
	else:
		flash('You have to log in before attempting any questions', at.red.value)
		return redirect(url_for('login'))

@app.route('/u', defaults={'path': ''})
@app.route('/u/<path:path>', methods=["GET", "POST"])
def catch_all_users(path):
	solved_challenges = []
	user = User.query.filter_by(username=path).first()
	if user is None:
		return abort(404)
	for challenge in user.solved_challenges:
		solved_challenges.append(challenge)
	return render_template("user_info.html", solved_challenges = solved_challenges, user = user)

if __name__ == "__main__":
	app.run(threaded=True, debug=True, host="0.0.0.0")
