from flask import *
from extensions import connect_to_database
from datetime import *
import hashlib
import uuid
import re

offerHelp = Blueprint('offerHelp', __name__, template_folder='templates')

@offerHelp.route('/offerHelp', methods=['GET', 'POST'])
def offerHelp_route():
	options = {
		"edit": False
	}
	if 'username' not in session:
		return redirect(url_for('user.login_route'))

	data = ''
	logged_in_data = ''
	db = connect_to_database()
	cur = db.cursor()
	cur.execute('SELECT firstname, lastname, userid, dogid FROM User WHERE username = \"' + session['username'] + '\"')
	result = cur.fetchall()
	cur.close()
	result = result[0]
	firstname = result['firstname']
	lastname = result['lastname']
	logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.user_route') + '>%s %s</a></li>' % (firstname, lastname)
	logged_in_data += '<li class="nav-item"><form method=\"POST\" action=\"%s\" id=nav_logout>' % (url_for('user.logout_route'))
	logged_in_data += '<button type=\"submit\">Logout</button><br/>'
	logged_in_data += '</form></li>'

	if request.method == 'POST':
		error = False
		error_msg = ""
		if 'helpdate' in request.form:
			if request.form['helpdate'] == "":
				error_msg += "<p class=\"error\">Help Date may not be left blank</p>"
				error = True
			if error:
				return render_template("offerHelp.html", logged_in_data=logged_in_data, data=data, error_data=error_msg, **options)
			
			helpDate = request.form['helpdate']
			helpDate = datetime.strptime(helpDate, "%m/%d/%Y").strftime('%Y-%m-%d')
			cur = db.cursor()
			cur.execute('INSERT INTO EventOffer(careType, eventDate, userid, status) VALUES(\"%s\", \"%s\", \"%d\", \"%s\")' % (request.form['petCare'], helpDate, result['userid'], 'offered'))
			cur.close()
			cur = db.cursor()
			cur.execute('SELECT eventDate, careType FROM EventRequest WHERE eventDate = \"' + helpDate + '\"')
			result2 = cur.fetchall()
			cur.close()

			
			data += '<form method=\"POST\">'
			data += 'Please select a pet care option: <select name="petCare">'
			data += '<option value="Playing">Playing</option>'
			data += '<option value="Sitting">Sitting</option>'
			data += '<option value="Grooming" selected="selected">Grooming</option>'
			data += '<option value="Walking">Walking</option>'
			data += '</select></br>'
			data += 'Select a Date Where You Are Free to Help: <input type="text" name="helpdate" value="" id="datepicker">'
			data +=	'<button type="submit" id=select_help_date>Submit</button>'
			data += '</form>'
			data += '<br>Your Matches:<br>'

			if len(result2) == 0:
				data += 'No Matches were found. Please try again.'

			else:
				data += '<table>'
				data += '<tr><th>Event Date</th><th>Care Type</th></tr>'
				for r in result2:
					data += '<tr><td>' + r['eventDate'] + '</td><td>' + r['careType'] + '</td></tr>'
				data += '</table>'
			return render_template("offerHelp.html", logged_in_data=logged_in_data, data=data, **options)

	else:
		data += '<form method=\"POST\">'
		data += 'Please select a pet care option: <select name="petCare">'
		data += '<option value="Playing">Playing</option>'
		data += '<option value="Sitting">Sitting</option>'
		data += '<option value="Grooming">Grooming</option>'
		data += '<option value="Walking">Walking</option>'
		data += '</select></br>'
		data += 'Select a Date Where You Are Free to Help: <input type="text" name="helpdate" value="" id="datepicker">'
		data +=	'<button type="submit" id=select_help_date>Submit</button>'
		data += '</form>'
		return render_template("offerHelp.html", logged_in_data=logged_in_data, data=data, **options)
