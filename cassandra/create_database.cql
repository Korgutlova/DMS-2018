-- version 1.0.0

DROP KEYSPACE IF EXISTS avia;

CREATE KEYSPACE avia 
	WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};


CREATE TABLE avia.airlines(
	id uuid PRIMARY KEY,
	name varchar,
	ICAO varchar
);

-- INSERT INTO avia.airlines (id, name, ICAO) VALUES (now(), 'smth', 'smth');


CREATE TABLE avia.cities (
    id uuid PRIMARY KEY,
	name varchar,
	longitude decimal,
	latitude decimal
); 

CREATE TABLE avia.airports (
	id uuid PRIMARY KEY,
	name varchar,
	city_id uuid

-- IN CQL NOT FOREIGN KEY...
); 

CREATE TABLE avia.airplanes(
	id uuid PRIMARY KEY,
	name  varchar,
	seats  int,
	mark varchar,
	term_of_use int,
	airline_id uuid
-- FK
);

CREATE TABLE avia.flight (
 	flight_number varchar PRIMARY KEY, 
  	from_city_id uuid,
-- FK
  	to_city_id uuid,
-- FK
  	airplane_id uuid,
-- FK
  	day int,
  	tense text,
-- change time -> text
  	duration int
);

CREATE TABLE avia.passengers(
	email varchar PRIMARY KEY,
	passport_data varchar,
	last_name varchar,
	first_name varchar,
	third_name varchar,
	date_birth varchar,
-- maybe timestamp
	gender varchar,
	password varchar
);


CREATE TABLE avia.counter_reservations(
	flight_number varchar,
	tense timestamp,
	amount_reservations counter,
	PRIMARY KEY (flight_number, tense)
);

CREATE TYPE avia.passport(
	email varchar,
	last_name varchar,
	first_name varchar,
	third_name varchar
);

CREATE TYPE avia.ticket(
	type text,
	place text,
	price decimal, 
	flight_no text,
	passport_data passport,
);

CREATE TABLE avia.reservation(
    passenger varchar,
    date timestamp,
    tickets list<ticket>
    PRIMARY KEY (passenger, date)
);

/*CREATE TABLE avia.flight_data(
    pk varchar PRIMARY KEY,
    data text
);
*/

