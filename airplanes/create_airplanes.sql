CREATE TABLE airplanes(
	id serial primary key,
	name  varchar(100),
	seats  int,
	mark varchar(100),
	term_of_use int,
	airline_id integer references airlines (id)
);



create or replace function update_airplanes() returns void as
$$
DECLARE
	c1 CURSOR FOR SELECT * FROM airplanes;
    id_list INT[];
    cur_air RECORD;
    n integer;
BEGIN		
   OPEN c1;
   select array_agg(id) into id_list from airlines order by random() limit 1;
   n := array_length(id_list, 1);
   LOOP
   	  FETCH c1 INTO cur_air;
      EXIT WHEN NOT FOUND;
      UPDATE airplanes SET airline_id = id_list[floor(random() * n)] WHERE cur_air.id=id;
   END LOOP;
   CLOSE c1;
END;
$$ language plpgsql;


COPY airplanes (name, seats, mark, term_of_use) FROM 'C:/data/airplanes.csv' WITH (FORMAT csv, header);
select update_airplanes();