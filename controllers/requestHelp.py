from flask import *

requestHelp = Blueprint('requestHelp', __name__, template_folder='templates')


@requestHelp.route('/requestHelp')
def requestHelp_route():
	options = {
		"edit": False
	}
	return render_template("requestHelp.html", **options)
