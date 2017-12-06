from flask import *

from extensions import connect_to_database

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():
	logged_in_data = ''
	data = ''
	if 'username' in session:
		username = session['username']
		db = connect_to_database()
		cur = db.cursor()
		cur.execute('SELECT firstname, lastname FROM User WHERE username = \"' + username + '\"')
		result = cur.fetchall()
		cur.close()
		result = result[0]
		firstname = result['firstname']
		lastname = result['lastname']
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.user_route') + '>%s %s</a></li>' % (firstname, lastname)
		logged_in_data += '<li class="nav-item"><form method=\"POST\" action=\"%s\" id=nav_logout>' % (url_for('user.logout_route'))
		logged_in_data += '<button type=\"submit\">Logout</button><br/>'
		logged_in_data += '</form></li>'

		data += '<p class="center"><h3 style="text-align: center">Welcome ' + firstname + ' ' + lastname + '</h3></p><br>'
		data += '<form action="/offerHelp"><input type="submit" class="btn btn-primary btn-lg btn-block" value="Help Someone Else Out" /></form><hr>'
		data += '<form action="/requestHelp"><input type="submit" class="btn btn-secondary btn-lg btn-block" value="Request Some Help" /></form>'
	else:
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.login_route') + ' id=home_login>Login</a></li>'
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.user_create_route') + ' id=home_user_create>Sign Up</a></li>'

		data += '<p class="center"><h3>Welome to PuppyPro!<br> Please log in or sign up!</h3></p><br>'
		data += '<form action=\"%s\"><input type="submit" class="btn btn-primary btn-lg btn-block" value="Login" /></form><hr>' % (url_for('user.login_route'))
		data += '<form action=\"%s\"><input type="submit" class="btn btn-secondary btn-lg btn-block" value="Sign Up" /></form>' % (url_for('user.user_create_route'))

		
	return render_template("index.html", logged_in_data=logged_in_data, data=data)


@main.route('/about')
def about_route():
	logged_in_data = ''
	if 'username' in session:
		db = connect_to_database()
		cur = db.cursor()
		cur.execute('SELECT firstname, lastname FROM User WHERE username = \"' + session['username'] + '\"')
		result = cur.fetchall()
		cur.close()
		result = result[0]
		firstname = result['firstname']
		lastname = result['lastname']
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.user_route') + '>%s %s</a></li>' % (firstname, lastname)
		logged_in_data += '<li class="nav-item"><form method=\"POST\" action=\"%s\" id=nav_logout>' % (url_for('user.logout_route'))
		logged_in_data += '<button type=\"submit\">Logout</button><br/>'
		logged_in_data += '</form></li>'
	else:
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.login_route') + ' id=home_login>Login</a></li>'
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.user_create_route') + ' id=home_user_create>Sign Up</a></li>'


	return render_template("about.html", logged_in_data=logged_in_data)

@main.route('/contact')
def contact_route():
	logged_in_data = ''
	if 'username' in session:
		db = connect_to_database()
		cur = db.cursor()
		cur.execute('SELECT firstname, lastname FROM User WHERE username = \"' + session['username'] + '\"')
		result = cur.fetchall()
		cur.close()
		result = result[0]
		firstname = result['firstname']
		lastname = result['lastname']
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.user_route') + '>%s %s</a></li>' % (firstname, lastname)
		logged_in_data += '<li class="nav-item"><form method=\"POST\" action=\"%s\" id=nav_logout>' % (url_for('user.logout_route'))
		logged_in_data += '<button type=\"submit\">Logout</button><br/>'
		logged_in_data += '</form></li>'
	else:
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.login_route') + ' id=home_login>Login</a></li>'
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.user_create_route') + ' id=home_user_create>Sign Up</a></li>'


	return render_template("contact.html", logged_in_data=logged_in_data)

@main.route('/services')
def services_route():
	logged_in_data = ''
	if 'username' in session:
		db = connect_to_database()
		cur = db.cursor()
		cur.execute('SELECT firstname, lastname FROM User WHERE username = \"' + session['username'] + '\"')
		result = cur.fetchall()
		cur.close()
		result = result[0]
		firstname = result['firstname']
		lastname = result['lastname']
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.user_route') + '>%s %s</a></li>' % (firstname, lastname)
		logged_in_data += '<li class="nav-item"><form method=\"POST\" action=\"%s\" id=nav_logout>' % (url_for('user.logout_route'))
		logged_in_data += '<button type=\"submit\">Logout</button><br/>'
		logged_in_data += '</form></li>'
	else:
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.login_route') + ' id=home_login>Login</a></li>'
		logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.user_create_route') + ' id=home_user_create>Sign Up</a></li>'


	return render_template("services.html", logged_in_data=logged_in_data)


