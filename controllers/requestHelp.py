from flask import *
from extensions import connect_to_database
from datetime import *
import hashlib
import uuid
import re

requestHelp = Blueprint('requestHelp', __name__, template_folder='templates')


@requestHelp.route('/requestHelp', methods=['GET', 'POST'])
def requestHelp_route():
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

	data += '<form method=\"POST\">'
	data += 'Please select a pet care option: <select name="petCare">'
	data += '<option value="Playing">Playing</option>'
	data += '<option value="Sitting">Sitting</option>'
	data += '<option value="Grooming">Grooming</option>'
	data += '<option value="Walking">Walking</option>'
	data += '</select></br>'
	data += 'Select a Date Where You Would Like a Hand: <input type="text" name="requestdate" value="" id="datepicker">'
	data +=	'<button type="submit" id=select_help_date>Submit</button>'
	data += '</form>'

	if request.method == 'POST':
		error = False
		error_msg = ""
		if 'requestdate' in request.form:
			if request.form['requestdate'] == "":
				error_msg += "<p class=\"error\">Request Date may not be left blank</p>"
				error = True
			if error:
				return render_template("requestHelp.html", logged_in_data=logged_in_data, data=data, error_data=error_msg, **options)
			
			requestDate = request.form['requestdate']
			requestDate = datetime.strptime(requestDate, "%m/%d/%Y").strftime('%Y-%m-%d')
			cur = db.cursor()
			cur.execute('INSERT INTO EventRequest(careType, eventDate, userid, dogid, status) VALUES(\"%s\", \"%s\", \"%d\", \"%d\", \"%s\")' % (request.form['petCare'], requestDate, result['userid'], result['dogid'], 'offered'))
			cur.close()
			cur = db.cursor()
			cur.execute('SELECT eventid, eventDate, careType FROM EventOffer WHERE eventDate = \"' + requestDate + '\"')
			result2 = cur.fetchall()
			cur.close()

			
			data = '<form method=\"POST\">'
			data += 'Please select a pet care option: <select name="petCare">'
			data += '<option value="Playing">Playing</option>'
			data += '<option value="Sitting">Sitting</option>'
			data += '<option value="Grooming">Grooming</option>'
			data += '<option value="Walking">Walking</option>'
			data += '</select></br>'
			data += 'Select a Date Where You Would Like a Hand: <input type="text" name="requestdate" value="" id="datepicker">'
			data +=	'<button type="submit" id=select_help_date>Submit</button>'
			data += '</form>'
			data += '<br>Your Matches:<br>'

			if len(result2) == 0:
				data += 'No Helpers were found. Please try again.'

			else:
				data += '<table style="width:100%">'
				data += '<tr><th align="left">Event Date</th><th align="left">Care Type</th><th>Choose your match</th></tr>'
				for r in result2:
					data += '<tr><td>' + str(r['eventDate']) + '</td>'
					data += '<td>' + r['careType'] + '</td>'
					data += '<td>'
					data += '<form method=\"POST\">'
					data += '<input type="hidden" name="eventid" value=' + str(r['eventid']) + '>'
					data +=	'<button type="submit" id=select_help_date>Select</button>'
					data += '</form></td></tr>'
				data += '</table>'
			return render_template("requestHelp.html", logged_in_data=logged_in_data, data=data, **options)

		if 'eventid' in request.form:
			eId = request.form['eventid']
			print('eventID: ' + eId)

			cur = db.cursor()
			cur.execute('SELECT userid, eventDate, careType FROM EventOffer WHERE eventid = \"' + eId + '\"')
			res = cur.fetchall()
			cur.close()
			res = res[0]

			cur = db.cursor()
			cur.execute('SELECT firstname, lastname FROM User WHERE userid = \"' + str(res['userid']) + '\"')
			res2 = cur.fetchall()
			cur.close()
			res2 = res2[0]


			data = '<div><center><hr><h3>You have selected</h3><h2><strong>' + res2['firstname'] + ' ' + res2['lastname'] + '</strong></h2>'
			data += '<h3>for your Dog ' + res['careType'] + ' needs</h3>'
			data += '<h3> On ' + str(res['eventDate']) + '</h3><hr>'
			data += '<h3>Please wait for a confirmation email</h3>'
			data += '<h3>Thank you for using Puppy Pro</h3></center></div><br><br>'
			return render_template("results.html", logged_in_data=logged_in_data, data=data, **options)


	else:
		return render_template("requestHelp.html", logged_in_data=logged_in_data, data=data, **options)


