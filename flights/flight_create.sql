create table if not exists cities
(
  id        serial not null
    constraint cities_pkey
    primary key,
  name      varchar(100),
  longitude numeric,
  latitude  numeric
);

create table if not exists airports
(
  id      serial not null
    constraint airports_pkey
    primary key,
  name    varchar(100),
  city_id integer
    constraint airports_city_id_fkey
    references cities
);

create table flight
(
  flight_number varchar(30) not null
    constraint flight_pkey
    primary key,
  from_city_id  integer
    constraint flight_from_city_id_fkey
    references cities
    constraint check_master
    check ((from_city_id >= 0) AND (from_city_id <= 12893)),
  to_city_id    integer
    constraint flight_to_city_id_fkey
    references cities,
  airplane_id   integer,
  day           integer
    constraint flight_day_check
    check ((day > 0) AND (day < 8)),
  tense         time        not null,
  duration      integer     not null,
  constraint unique_constr_flight
  unique (flight_number, from_city_id, to_city_id, airplane_id, day, tense)
);

create index newest_master
  on flight (from_city_id);

create function inheritf()
  returns trigger
language plpgsql
as $$
DECLARE
  new_table_name varchar;
  num            int;
BEGIN
  num = NEW.from_city_id % 10;
  new_table_name = 'flight_' || num;

  EXECUTE ('CREATE TABLE if not exists ' || new_table_name ||
           ' ( check ( from_city_id % 10  = ' || num || ')) inherits (flight)');
  EXECUTE ('insert into ' || new_table_name || '  values ('''
           || NEW.flight_number || ''', '
           || NEW.from_city_id || ', '
           || NEW.to_city_id || ', '
           || NEW.airplane_id || ', '
           || NEW.day || ', '''
           || NEW.tense || ''', '
           || NEW.duration || ' );');
  return null;
END
$$;

alter function inheritf()
  owner to postgres;

create trigger inherittrigger
  before insert
  on flight
  for each row
execute procedure inheritf();

