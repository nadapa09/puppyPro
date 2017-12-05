CREATE TABLE User(userid INT AUTO_INCREMENT, username VARCHAR(20), type VARCHAR(5), firstname VARCHAR(20), lastname VARCHAR(20), email VARCHAR(40), dogid INT, password VARCHAR(20), PRIMARY KEY(userid));

CREATE TABLE Dog(dogid INT AUTO_INCREMENT, name VARCHAR(10), breed VARCHAR(50), age INT, PRIMARY KEY(dogid));  

CREATE TABLE Event(eventid INT AUTO_INCREMENT, currentDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, eventDate DATE, userid_owner INT, userid_lover INT, dogid INT, status VARCHAR(100), PRIMARY KEY(eventid));


