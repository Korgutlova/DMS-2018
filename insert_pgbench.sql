\set aid (random(1, 1000000 * :scale))
BEGIN;
SELECT * FROM flight_data as f WHERE f.id=:aid;
END;