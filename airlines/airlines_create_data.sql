CREATE TABLE airlines (
id serial primary key,
name varchar(120),
ICAO varchar(20)
);

CREATE OR REPLACE FUNCTION random_string_timur(int)
RETURNS text
AS $$
  SELECT array_to_string(
    ARRAY (
      SELECT substring(
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        FROM (random() *26)::int FOR 1)
      FROM generate_series(1, $1) ), '' )
$$ LANGUAGE sql;

-- Change the path to your csv
COPY airlines (name, ICAO)  FROM '/Users/timurtimerhanov/PycharmProjects/SUBD/airlines.csv' WITH (FORMAT csv);