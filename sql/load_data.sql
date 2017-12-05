INSERT INTO User(username, type, firstname, lastname, email, dogid, password) VALUES ('DinaD', 'owner', 'Dina', 'TheDogOwner', 'DinaTheDogOwner@gmail.com', 1, '123abc');

INSERT INTO User(username, type, firstname, lastname, email, dogid, password) VALUES ('nadapa', 'owner', 'Nithin', 'Adapa', 'adapa@umich.edu', 2, '123abc');

INSERT INTO User(username, type, firstname, lastname, email, password) VALUES ('svale', 'lover', 'Shounak', 'Vale', 'svale@umich.edu', '123abc');

INSERT INTO User(username, firstname, lastname, email, password) VALUES ('dscheng', 'David', 'Cheng', 'dscheng@umich.edu', '123456');

INSERT INTO Dog(name, breed, age) VALUES ('Sammy', 'Shih-Tzu', 1);

INSERT INTO Dog(name, breed, age) VALUES ('Lucky', 'Shih-Tzu', 2);

INSERT INTO Event(eventDate, userid_owner, userid_lover, dogid, status) VALUES ('12/04/17', 1, 3, 1, 'scheduled');

INSERT INTO Event(eventDate, userid_owner, userid_lover, dogid, status) VALUES ('12/04/17', 2, 3, 1, 'scheduled');

