from blueprints import *
db.create_all()
db.session.commit()
app.run(debug=True)