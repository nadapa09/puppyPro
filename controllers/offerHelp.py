from flask import *

offerHelp = Blueprint('offerHelp', __name__, template_folder='templates')

@offerHelp.route('/offerHelp')
def offerHelp_route():
	options = {
		"edit": False
	}
	return render_template("offerHelp.html", **options)
