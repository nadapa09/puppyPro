from flask import *

results = Blueprint('results', __name__, template_folder='templates')

@results.route('/results')
def results_route():
	return render_template("results.html")