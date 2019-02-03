from blueprints import *

User.query.delete()
Challenge.query.delete()
Solved.query.delete()
db.session.commit()
