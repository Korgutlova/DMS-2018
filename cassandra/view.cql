INSERT INTO flight_data (time, flight_number, speed, height, remaining_distance, temperature_overboard, engine_condition, weather_condition) 
VALUES ('2016-10-8T11:12:05', 'CTAHE', 160.7, 1023.4, 300, -40.5, 'normal', 'sunny');

SELECT * from flight_data where flight_number='CTAHE' and time=toTimestamp(now()) and remaining_distance < 50 ALLOW FILTERING;

CREATE MATERIALIZED VIEW avia.flight_data_view 
	AS SELECT * 
	FROM avia.flight_data
	WHERE time IS NOT NULL AND flight_number IS NOT NULL AND  remaining_distance IS NOT NULL
		  PRIMARY KEY (time, flight_number, remaining_distance);

INSERT INTO flight_data (time, flight_number, speed, height, remaining_distance, temperature_overboard, engine_condition, weather_condition) 
VALUES ('2016-12-8T11:12:05', 'CTAHE', 170.7, 1023.4, 300, -40.5, 'good', 'sunny');

SELECT * from flight_data_view where flight_number='CTAHE' and time=toTimestamp(now()) and remaining_distance < 50 ALLOW FILTERING;
