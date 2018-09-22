CREATE TABLE cities (
    id serial primary key,
	name varchar(100),
	longitude decimal,
	latitude decimal
); 

CREATE TABLE airports (
	id serial primary key,
	name varchar(100),
	city_id  integer references cities (id)
); 

create or replace function random_string(length integer) returns text as
$$
declare
  chars text[] := '{A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}';
  result text := '';
  i integer := 0;
begin
  if length < 0 then
    raise exception 'Given length cannot be less than 0';
  end if;
  for i in 1..length loop
    result := result || chars[1+random()*(array_length(chars, 1)-1)];
  end loop;
  return result;
end;
$$ language plpgsql;


create or replace function update_airports() returns void as
$$
DECLARE
	c1 CURSOR FOR SELECT * FROM airports;
    id_list INT[];
    cur_air RECORD;
    n integer;
BEGIN		
   OPEN c1;
   select array_agg(id) into id_list from cities order by random() limit 1;
   n := array_length(id_list, 1);
   LOOP
   	  FETCH c1 INTO cur_air;
      EXIT WHEN NOT FOUND;
      UPDATE airports SET city_id = id_list[floor(random() * n)] WHERE cur_air.id=id;
   END LOOP;
   CLOSE c1;
END;
$$ language plpgsql;

-- Замените на ваш путь до файлов csv
COPY cities (name, latitude, longitude) FROM '/Users/timurtimerhanov/PycharmProjects/SUBD/cities_and_airports/worldcities.csv' (FORMAT CSV, DELIMITER(','), HEADER);

-- Замените на ваш путь до файлов csv
COPY airports (name) FROM '/Users/timurtimerhanov/PycharmProjects/SUBD/cities_and_airports/airports.csv' (FORMAT CSV, DELIMITER(','), HEADER);

select update_airports();
