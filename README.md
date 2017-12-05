Puppy Pro

Instructions to Run the code

1. Make sure you have virtual box installed
2. Enter Terminal and enter the following commands
	vagrant up
	vagrant ssh
	cd /vagrant
	virtualenv venv
	source venv/bin/activate

3. Set up the database with the following commands. You will be prompted to enter password after each line. Password is root.
	mysql -u root -p puppypro_db < /vagrant/sql/tbl_drop.sql
	mysql -u root -p puppypro_db < /vagrant/sql/load_data.sql
	mysql -u root -p puppypro_db < /vagrant/sql/tbl_create.sql
	
