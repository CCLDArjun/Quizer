from blueprints import *
import os
import sys

if os.getuid() != 0:
	print("Quizer requires sudo/admin privledges")
	sys.exit()

db.create_all()
db.session.commit()
app.run(debug=True)