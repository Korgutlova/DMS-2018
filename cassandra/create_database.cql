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
	first_name varchar,
	last_name varchar,
	third_name varchar
);

CREATE TYPE avia.ticket(
	type int,
	place text,
	price decimal, 
	flight_number text,
	passport_data frozen<passport>
);

CREATE TABLE avia.reservation(
    passenger varchar,
    date timestamp,
    tickets list<frozen<ticket>>,
    PRIMARY KEY ((passenger), date)
);

CREATE TABLE avia.flight_data(
    time timestamp,
    flight_number text,
    speed decimal,
    height decimal,
    remaining_distance decimal,
    temperature_overboard decimal,
    engine_condition  text,
    weather_condition text,
    PRIMARY KEY (flight_number, time)
);


INSERT INTO reservation (passenger, date, tickets ) VALUES ( 'pass1', toTimestamp(now()), [
    {
        type: 12,
        place: 'asdasdasd',
        price: 213.3,
        flight_number: 'asdasd',
        passport_data: {
            email: 'asdasdas',
            first_name: 'asdasdas',
            last_name: 'asdasd',
            third_name: 'asdasdasd'
        }
    }
]);
