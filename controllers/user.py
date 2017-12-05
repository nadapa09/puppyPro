from flask import *

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/user')
def user_route():
	options = {
		"edit": False
	}
	return render_template("user.html", **options)