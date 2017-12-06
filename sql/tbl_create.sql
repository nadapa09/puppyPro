CREATE TABLE User(userid INT AUTO_INCREMENT, username VARCHAR(20), type VARCHAR(5), firstname VARCHAR(20), lastname VARCHAR(20), email VARCHAR(40), dogid INT, password VARCHAR(20), PRIMARY KEY(userid));

CREATE TABLE Dog(dogid INT AUTO_INCREMENT, name VARCHAR(10), breed VARCHAR(50), age INT, PRIMARY KEY(dogid));  

CREATE TABLE EventRequest(eventid INT AUTO_INCREMENT, careType VARCHAR(20), eventDate DATE, startTime VARCHAR(10), endTime VARCHAR(10), userid INT, dogid INT, status VARCHAR(20), PRIMARY KEY(eventid));

CREATE TABLE EventOffer(eventid INT AUTO_INCREMENT, careType VARCHAR(20), eventDate DATE, startTime VARCHAR(10), endTime VARCHAR(10), userid INT, status VARCHAR(20), PRIMARY KEY(eventid));

CREATE TABLE EventHistory(eventid INT AUTO_INCREMENT, eventid_request INT, eventid_offer INT, careType VARCHAR(20), eventDate DATE, startTime VARCHAR(10), endTime VARCHAR(10), userid_owner INT, userid_lover INT, dogid INT, status VARCHAR(20), PRIMARY KEY(eventid));
