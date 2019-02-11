from flask import current_app, abort, request, session, g

def admin(app):
	@app.before_request
	def admin_check():
		try:
			if session['username'] != "admin":
				abort(403)
		except KeyError:
			abort(403)
