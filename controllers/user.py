from flask import *
from extensions import connect_to_database
import hashlib
import uuid
import re

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/login', methods=['GET', 'POST'])
def login_route():
	if 'username' in session:
		return redirect(url_for('main.main_route'));
	else:
		db = connect_to_database()
		error_msg = ""
		error = False
		if request.method == 'POST':
			if request.form['username'] == "" and request.form['password'] == "":
				error_msg += "<p class=\"error\">Username may not be left blank</p>"
				error_msg += "<p class=\"error\">Password may not be left blank</p>"
				print_str = '<form method=\"POST\">'
				print_str += 'Username: <input type=\"text\" id=login_username_input name=\"username\" value=\"\"><br/>'
				print_str += 'Password: <input type=\"password\" id=login_password_input name=\"password\" value=\"\"><br/>'
				print_str += '<button type=\"submit\" id=login_submit>Sign-in</button></form><br/>'
				return render_template("login.html", logged_in_data='', data=print_str, error_data=error_msg)

			elif request.form['username'] == "":
				error_msg += "<p class=\"error\">Username may not be left blank</p>"
				error = True
			elif request.form['password'] == "":
				error_msg += "<p class=\"error\">Password may not be left blank</p>"
				error = True

			cur = db.cursor()
			username = request.form['username']
			password = request.form['password']
			cur.execute(str('SELECT username FROM User WHERE username=\'' + username + '\''))
			user_exists = cur.fetchall()
			if len(user_exists) == 0 and request.form['username'] != "":
				error_msg += "<p class=\"error\">Username does not exist</p>"
				error = True

			if error:
				# print ("some error exists. rerendering login page with error statements")
				print_str = '<form method=\"POST\">'
				print_str += 'Username: <input type=\"text\" id=login_username_input name=\"username\" value=\"\"><br/>'
				print_str += 'Password: <input type=\"password\" id=login_password_input name=\"password\" value=\"\"><br/>'
				print_str += '<button type=\"submit\" id=login_submit>Sign-in</button></form><br/>'
				return render_template("login.html", logged_in_data='', data=print_str, error_data=error_msg)

			# To verify password, hash input password with provided salt and compare
			cur.execute(str('SELECT password FROM User WHERE username = \'' + username + '\''))
			true_password = cur.fetchall()
			cur.close()
			if password != true_password[0]['password']:
				# print ("hashed password is not the same as actual password")
				error_msg += "<p class=\"error\">Password is incorrect for the specified username</p>"
				print_str = '<form method=\"POST\">'
				print_str += 'Username: <input type=\"text\" id=login_username_input name=\"username\" value=\"\"><br/>'
				print_str += 'Password: <input type=\"password\" id=login_password_input name=\"password\" value=\"\"><br/>'
				print_str += '<button type=\"submit\" id=login_submit>Sign-in</button></form><br/>'
				return render_template("login.html", logged_in_data='', data=print_str, error_data=error_msg)
			else:
				session['username'] = username
				return redirect(url_for('main.main_route'))

		else:
			# print ("request method does not equal post")
			print_str = '<form method=\"POST\">'
			print_str += 'Username: <input type=\"text\" id=login_username_input name=\"username\" value=\"\"><br/>'
			print_str += 'Password: <input type=\"password\" id=login_password_input name=\"password\" value=\"\"><br/>'
			print_str += '<button type=\"submit\" id=login_submit>Sign-in</button></form><br/>'
			return render_template("login.html", logged_in_data='', data=print_str, error_data='')
	
@user.route('/logout', methods=['GET', 'POST'])
def logout_route():
	if request.method == 'POST':
		session.pop('username', None)
		return redirect(url_for('main.main_route'));
	else:
		abort(403)

@user.route('/user/create', methods=['GET', 'POST'])
def user_create_route():
	if 'username' in session:
		return redirect(url_for('user.user_route'))

	options = {
		"edit": False,
		"createUser": True
	}
	db = connect_to_database()
	error_msg = ""
	error = False

	if request.method == 'POST':
		if request.form['username'] == "":
			error_msg += "<p class=\"error\">Username may not be left blank</p>"
			error = True
		if request.form['firstname'] == "":
			error_msg += "<p class=\"error\">Firstname may not be left blank</p>"
			error = True
		if request.form['lastname'] == "":
			error_msg += "<p class=\"error\">Lastname may not be left blank</p>"
			error = True
		if request.form['password1'] == "":
			error_msg += "<p class=\"error\">Password1 may not be left blank</p>"
			error = True
		if request.form['email'] == "":
			error_msg += "<p class=\"error\">Email may not be left blank</p>"
			error = True

		if len(request.form['username']) > 20:
			error_msg += "<p class=\"error\">Username must be no longer than 20 characters</p>"
			error = True
		if len(request.form['firstname']) > 20:
			error_msg += "<p class=\"error\">Firstname must be no longer than 20 characters</p>"
			error = True
		if len(request.form['lastname']) > 20:
			error_msg += "<p class=\"error\">Lastname must be no longer than 20 characters</p>"
			error = True

		cur = db.cursor()
		cur.execute(str('SELECT username FROM User WHERE username=\'' + request.form['username'] + '\''))
		result = cur.fetchall()
		cur.close()
		if len(result) != 0:
			error_msg += "<p class=\"error\">This username is taken</p>"
			error = True


		if len(request.form['username']) < 3:
			error_msg += "<p class=\"error\">Usernames must be at least 3 characters long</p>"
			error = True

		if not re.match("^[A-Za-z0-9_]*$", request.form['username']):
			error_msg += "<p class=\"error\">Usernames may only contain letters, digits, and underscores</p>"
			error = True

		if len(request.form['password1']) < 8:
			error_msg += "<p class=\"error\">Passwords must be at least 8 characters long</p>"
			error = True

		if not bool(re.search(r'[a-zA-Z]', request.form['password1'])) or not bool(re.search(r'[0-9]', request.form['password1'])):
			error_msg += "<p class=\"error\">Passwords must contain at least one letter and one number</p>"
			error = True

		if not re.match("^[A-Za-z0-9_]*$", request.form['password1']):
			error_msg += "<p class=\"error\">Passwords may only contain letters, digits, and underscores</p>"
			error = True

		if not re.match(r"[^@]+@[^@]+\.[^@]+", request.form['email']):
			error_msg += "<p class=\"error\">Email address must be valid</p>"
			error = True

		if len(request.form['email']) > 40:
			error_msg += "<p class=\"error\">Email must be no longer than 40 characters</p>"
			error = True

		if request.form['password1'] != request.form['password2']:
			error_msg += "<p class=\"error\">Passwords do not match</p>"
			error = True

		if error:
			print_str = '<form method=\"POST\">'
			print_str += 'Username: <input type=\"text\" id=new_username_input name=\"username\" value=\"\"><br/>'
			print_str += 'First Name: <input type=\"text\" id=new_firstname_input name=\"firstname\" value=\"\"><br/>'
			print_str += 'Last Name: <input type=\"text\" id=new_lastname_input name=\"lastname\" value=\"\"><br/>'
			print_str += 'Password: <input type=\"password\" id=new_password1_input name=\"password1\" value=\"\"><br/>'
			print_str += 'Confirm Password: <input type=\"password\" id=new_password2_input name=\"password2\" value=\"\"><br/>'
			print_str += 'Email: <input type=\"text\" id=new_email_input name=\"email\" value=\"\"><br/>'
			print_str += '<button type=\"submit\" id =new_submit>Create User</button></form><br/>'
			return render_template("user.html", logged_in_data='', data=print_str, error_data=error_msg, **options)

		username = request.form['username']
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		password = request.form['password1']
		email = request.form['email']

		cur = db.cursor()
		cur.execute('INSERT INTO User(username, firstname, lastname, password, email) VALUES(\"%s\", \"%s\", \"%s\", \"%s\", \"%s\")' % (username, firstname, lastname, password, email))
		cur.close()
		return redirect(url_for('user.login_route'))

	else:
		print_str = '<form method=\"POST\">'
		print_str += 'Username: <input type=\"text\" id=new_username_input name=\"username\" value=\"\"><br/>'
		print_str += 'First Name: <input type=\"text\" id=new_firstname_input name=\"firstname\" value=\"\"><br/>'
		print_str += 'Last Name: <input type=\"text\" id=new_lastname_input name=\"lastname\" value=\"\"><br/>'
		print_str += 'Password: <input type=\"password\" id=new_password1_input name=\"password1\" value=\"\"><br/>'
		print_str += 'Confirm Password: <input type=\"password\" id=new_password2_input name=\"password2\" value=\"\"><br/>'
		print_str += 'Email: <input type=\"text\" id=new_email_input name=\"email\" value=\"\"><br/>'
		print_str += '<button type=\"submit\" id=new_submit>Create User</button></form><br/>'
		return render_template("user.html", logged_in_data='', data=print_str, error_data='', **options)

@user.route('/user/addDog', methods=['GET', 'POST'])
def user_add_dog_route():
	options = {
		"edit": False
	}
	if 'username' not in session:
		return redirect(url_for('user.login_route'))

	logged_in_data = ''
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

	error_msg = ""
	error = False

	if request.method == 'POST':
		if request.form['dogName'] == "":
			error_msg += "<p class=\"error\">Dog Name may not be left blank</p>"
			error = True
		if request.form['dogBreed'] == "":
			error_msg += "<p class=\"error\">Dog Breed may not be left blank</p>"
			error = True
		if request.form['dogAge'] == "":
			error_msg += "<p class=\"error\">Dog Age may not be left blank</p>"
			error = True
		if len(request.form['dogName']) > 10:
			error_msg += "<p class=\"error\">Dog Name must be no longer than 10 characters</p>"
			error = True
		if len(request.form['dogBreed']) > 50:
			error_msg += "<p class=\"error\">Dog Breed must be no longer than 50 characters</p>"
			error = True
		if not request.form['dogAge'].isdigit():
			error_msg += "<p class=\"error\">Dog Age must be a number</p>"
			error = True

		if error:
			print_str = '<form method=\"POST\">'
			print_str += 'Name: <input type=\"text\" id=new_dogname_input name=\"dogName\" value=\"\"><br/>'
			print_str += 'Breed: <input type=\"text\" id=new_dogbreed_input name=\"dogBreed\" value=\"\"><br/>'
			print_str += 'Age: <input type=\"text\" id=new_dogage_input name=\"dogAge\" value=\"\"><br/>'
			print_str += '<button type=\"submit\" id=new_submit>Add Dog</button></form><br/>'
			return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data=error_msg, **options)

		dogName = request.form['dogName']
		dogBreed = request.form['dogBreed']
		dogAge = int(request.form['dogAge'])

		cur = db.cursor()
		cur.execute('INSERT INTO Dog(name, breed, age) VALUES(\"%s\", \"%s\", \"%d\")' % (dogName, dogBreed, dogAge))
		cur.close()

		cur = db.cursor()
		cur.execute('SELECT dogid FROM Dog WHERE name = \"' + dogName + '\"')
		result2 = cur.fetchall()
		cur.close()
		result2 = result2[0]

		cur = db.cursor()
		cur.execute(('UPDATE User SET dogid=\'' + str(result2['dogid']) + '\' WHERE username=\'' + session['username'] + '\''))
		cur.execute(('UPDATE User SET type=\'owner\' WHERE username=\'' + session['username'] + '\''))
		cur.close()

		return redirect(url_for('user.user_route'))

	else:
		print_str = '<form method=\"POST\">'
		print_str += 'Name: <input type=\"text\" id=new_dogname_input name=\"dogName\" value=\"\"><br/>'
		print_str += 'Breed: <input type=\"text\" id=new_dogbreed_input name=\"dogBreed\" value=\"\"><br/>'
		print_str += 'Age: <input type=\"text\" id=new_dogage_input name=\"dogAge\" value=\"\"><br/>'
		print_str += '<button type=\"submit\" id=new_submit>Add Dog</button></form><br/>'
		return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data='', **options)

@user.route('/user')
def user_route():
	options = {
		"edit": False
	}
	if 'username' not in session:
		return redirect(url_for('user.login_route'))

	logged_in_data = ''
	data = ''
	db = connect_to_database()
	cur = db.cursor()
	cur.execute('SELECT firstname, lastname, username, email, dogid FROM User WHERE username = \"' + session['username'] + '\"')
	result = cur.fetchall()
	cur.close()
	result = result[0]
	firstname = result['firstname']
	lastname = result['lastname']
	logged_in_data += '<li class="nav-item"><a class="nav-link" href=' + url_for('user.user_route') + '>%s %s</a></li>' % (firstname, lastname)
	logged_in_data += '<li class="nav-item"><form method=\"POST\" action=\"%s\" id=nav_logout>' % (url_for('user.logout_route'))
	logged_in_data += '<button type=\"submit\">Logout</button><br/>'
	logged_in_data += '</form></li>'

	data += '<h5>First Name: ' + result['firstname'] + '</h5>'
	data += '<h5>Last Name: ' + result['lastname'] + '</h5>'
	data += '<h5>User Name: ' + result['username'] + '</h5>'
	data += '<h5>Email: ' + result['email'] + '</h5>'

	if result['dogid'] is not None:
		cur = db.cursor()
		cur.execute('SELECT name, breed, age FROM Dog WHERE dogid = \"' + str(result['dogid']) + '\"')
		result2 = cur.fetchall()
		cur.close()
		result2 = result2[0]

		data += '<h5>Dog Name: ' + result2['name'] + '</h5>'
		data += '<h5>Dog Breed: ' + result2['breed'] + '</h5>'
		data += '<h5>Dog Age: ' + str(result2['age']) + '</h5><br>'
	else:
		data += '<br><form action=\"%s\"><input type="submit" class="btn btn-primary btn-lg btn-block" value="Add Dog Information" /></form><br>' % (url_for('user.user_add_dog_route'))

	data += '<form action=\"%s\"><input type="submit" class="btn btn-primary btn-lg btn-block" value="Edit Information" /></form><br>' % (url_for('user.user_edit_route'))

	return render_template("user.html", logged_in_data=logged_in_data, data=data, **options)

@user.route('/user/edit', methods=['GET', 'POST'])
def user_edit_route():
	options = {
		"edit": True,
		"createUser": False
	}
	if 'username' not in session:
		return redirect(url_for('user.login_route'))

	db = connect_to_database()
	error_msg = ""
	logged_in_data = ''
	login = ''
	error = False
	username = session['username']

	print_str = '<h5>Edit User Information</h5>'
	print_str += '<form method=\"POST\">'
	print_str += '<input type=\"hidden\" name=\"op\" value=\"edit\">'
	print_str += 'Edit First Name: <input type=\"text\" name=\"firstname\" value=\"\" id=update_firstname_input>'
	print_str += '<button type=\"submit\" id=update_firstname_submit>Update Firstname</button>'
	print_str += '</form>'

	print_str += '<form method=\"POST\">'
	print_str += '<input type=\"hidden\" name=\"op\" value=\"edit\">'
	print_str += 'Edit Last Name: <input type=\"text\" name=\"lastname\" value=\"\" id=update_lastname_input>'
	print_str += '<button type=\"submit\" id=update_lastname_submit>Update Lastname</button>'
	print_str += '</form>'

	print_str += '<form method=\"POST\">'
	print_str += '<input type=\"hidden\" name=\"op\" value=\"edit\">'
	print_str += 'Edit Email: <input type=\"text\" name=\"email\" value=\"\" id=update_email_input>'
	print_str += '<button type=\"submit\" id=update_email_submit>Update Email</button>'
	print_str += '</form>'

	print_str += '<form method=\"POST\">'
	print_str += '<input type=\"hidden\" name=\"op\" value=\"edit\">'
	print_str += 'New Password: <input type=\"password\" name=\"password1\" value=\"\" id=update_password1_input><br/>'
	print_str += 'Confirm New Password: <input type=\"password\" name=\"password2\" value=\"\" id=update_password2_input><br/>'
	print_str += '<button type=\"submit\" id=update_password_submit>Update Password</button>'
	print_str += '</form>'

	print_str += '<h5>Edit Dog Information</h5>'
	print_str += '<form method=\"POST\">'
	print_str += '<input type=\"hidden\" name=\"op\" value=\"edit\">'
	print_str += 'Dog Name: <input type=\"text\" name=\"dogName\" value=\"\" id=update_dog_name>'
	print_str += '<button type=\"submit\" id=update_dog_name>Update Dog Name</button>'
	print_str += '</form>'

	print_str += '<form method=\"POST\">'
	print_str += '<input type=\"hidden\" name=\"op\" value=\"edit\">'
	print_str += 'Dog Breed: <input type=\"text\" name=\"dogBreed\" value=\"\" id=update_dog_breed>'
	print_str += '<button type=\"submit\" id=update_dog_breed>Update Dog Breed</button>'
	print_str += '</form>'

	print_str += '<form method=\"POST\">'
	print_str += '<input type=\"hidden\" name=\"op\" value=\"edit\">'
	print_str += 'Dog Age: <input type=\"text\" name=\"dogAge\" value=\"\" id=update_dog_age>'
	print_str += '<button type=\"submit\" id=update_dog_age>Update Dog Age</button>'
	print_str += '</form>'

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

	if request.method == 'POST':
		if 'firstname' in request.form:
			if len(request.form['firstname']) > 20:
				error_msg += "<p class=\"error\">Firstname must be no longer than 20 characters</p>"
				error = True
			if error:
				return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data=error_msg, **options)
			cur = db.cursor()
			firstname = request.form['firstname']
			cur.execute(('UPDATE User SET firstname=\'' + firstname + '\' WHERE username=\'' + username + '\''))
			cur.close()
			return redirect(url_for('user.user_edit_route'))

		elif 'lastname' in request.form:
			if len(request.form['lastname']) > 20:
				error_msg += "<p class=\"error\">Lastname must be no longer than 20 characters</p>"
				error = True
			if error:
				return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data=error_msg, **options)
			cur = db.cursor()
			lastname = request.form['lastname']
			cur.execute(('UPDATE User SET lastname=\'' + lastname + '\' WHERE username=\'' + username + '\''))
			cur.close()
			return redirect(url_for('user.user_edit_route'))

		elif 'password1' in request.form:
			if len(request.form['password1']) < 8:
				error_msg += "<p class=\"error\">Passwords must be at least 8 characters long</p>"
				error = True
			if not bool(re.search(r'[a-zA-Z]', request.form['password1'])) or not bool(re.search(r'[0-9]', request.form['password1'])):
				error_msg += "<p class=\"error\">Passwords must contain at least one letter and one number</p>"
				error = True
			if not re.match("^[A-Za-z0-9_]*$", request.form['password1']):
				error_msg += "<p class=\"error\">Passwords may only contain letters, digits, and underscores</p>"
				error = True
			if request.form['password1'] != request.form['password2']:
				error_msg += "<p class=\"error\">Passwords do not match</p>"
				error = True
			if error:
				return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data=error_msg, **options)

			cur = db.cursor()
			password = request.form['password1']
			cur.execute(('UPDATE User SET password=\'' + password + '\' WHERE username=\'' + username + '\''))
			cur.close()
			return redirect(url_for('user.user_edit_route'))

		elif 'email' in request.form:
			if not re.match(r"[^@]+@[^@]+\.[^@]+", request.form['email']):
				error_msg += "<p class=\"error\">Email address must be valid</p>"
				error = True
			if len(request.form['email']) > 40:
				error_msg += "<p class=\"error\">Email must be no longer than 40 characters</p>"
				error = True
			if error:
				return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data=error_msg, **options)

			cur = db.cursor()
			email = request.form['email']
			cur.execute(('UPDATE User SET email=\'' + email + '\' WHERE username=\'' + username + '\''))
			cur.close()
			return redirect(url_for('user.user_edit_route'))

		else:
			cur = db.cursor()
			cur.execute('SELECT dogid FROM User WHERE username = \"' + session['username'] + '\"')
			result = cur.fetchall()
			cur.close()
			result = result[0]
			print(result['dogid'])
			if result is None:
				error_msg += "<p class=\"error\">No Dog Registered</p>"
				return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data=error_msg, **options)

			if 'dogName' in request.form:
				if len(request.form['dogName']) > 10:
					error_msg += "<p class=\"error\">Dog Name must be no longer than 10 characters</p>"
					error = True
				if error:
					return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data=error_msg, **options)
				cur = db.cursor()
				dogName = request.form['dogName']
				cur.execute(('UPDATE Dog SET name=\'' + dogName + '\' WHERE dogid=\'' + str(result['dogid']) + '\''))
				cur.close()
				return redirect(url_for('user.user_edit_route'))

			if 'dogBreed' in request.form:
				if len(request.form['dogBreed']) > 10:
					error_msg += "<p class=\"error\">Dog Breed must be no longer than 50 characters</p>"
					error = True
				if error:
					return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data=error_msg, **options)
				cur = db.cursor()
				dogBreed = request.form['dogBreed']
				cur.execute(('UPDATE Dog SET breed=\'' + dogBreed + '\' WHERE dogid=\'' + str(result['dogid']) + '\''))
				cur.close()
				return redirect(url_for('user.user_edit_route'))

			if 'dogAge' in request.form:
				if not request.form['dogAge'].isdigit():
					error_msg += "<p class=\"error\">Dog Age must be a number</p>"
					error = True
				if error:
					return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data=error_msg, **options)
				cur = db.cursor()
				dogAge = request.form['dogAge']
				cur.execute(('UPDATE Dog SET age=\'' + dogAge + '\' WHERE dogid=\'' + str(result['dogid']) + '\''))
				cur.close()
				return redirect(url_for('user.user_edit_route'))

	else:
		return render_template("user.html", logged_in_data=logged_in_data, data=print_str, error_data='', **options)


