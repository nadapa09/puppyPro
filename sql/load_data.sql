INSERT INTO User(username, type, firstname, lastname, email, dogid, password) VALUES ('DinaD', 'owner', 'Dina', 'TheDogOwner', 'DinaTheDogOwner@gmail.com', 1, '123abc');

INSERT INTO User(username, type, firstname, lastname, email, dogid, password) VALUES ('nadapa', 'owner', 'Nithin', 'Adapa', 'adapa@umich.edu', 2, '123abc');

INSERT INTO User(username, type, firstname, lastname, email, password) VALUES ('svale', 'lover', 'Shounak', 'Vale', 'svale@umich.edu', '123abc');

INSERT INTO User(username, firstname, lastname, email, password) VALUES ('dscheng', 'David', 'Cheng', 'dscheng@umich.edu', '123456');

INSERT INTO Dog(name, breed, age) VALUES ('Sammy', 'Shih-Tzu', 1);

INSERT INTO Dog(name, breed, age) VALUES ('Lucky', 'Shih-Tzu', 2);

INSERT INTO EventRequest(careType, eventDate, startTime, endTime, userid, dogid, status) VALUES ('Grooming', '17/12/04', '12:00', '24:00', 1, 1, 'requested');

INSERT INTO EventOffer(careType, eventDate, startTime, endTime, userid, status) VALUES ('Grooming', '17/12/04', '15:00', '18:00', 2, 'offered');

INSERT INTO EventHistory(eventid_request, eventid_offer, careType, eventDate, startTime, endTime, userid_owner, userid_lover, dogid, status) VALUES (1, 1, 'Grooming', '17/12/04', '15:00', '18:00', 1, 3, 1, 'scheduled');
