-- version 1.0.0

DROP KEYSPACE IF EXISTS avia;

CREATE KEYSPACE avia 
	WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};

CREATE TABLE avia.counter_reservations(
	flight_number varchar,
	-- tense timestamp,
	amount_reservations counter,
	PRIMARY KEY (flight_number)
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
	flight_number text,
	passport_data frozen<passport>
);

CREATE TABLE avia.reservation(
    passenger varchar,
    date timestamp,
    tickets list<frozen<ticket>>,
    PRIMARY KEY (passenger, date)
);


