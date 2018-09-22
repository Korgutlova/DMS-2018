INSERT INTO public.airports(name, city_id) VALUES 
	(random_string((floor(random() * 30) + 4)::integer), 
     (select id::integer 
     from cities
     order by random()
     limit 1));