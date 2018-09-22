INSERT INTO public.cities(name, latitude, longitude) 
	VALUES (random_string((floor(random() * 30) + 4)::integer), 
            (random() * 180 - 90), 
            (random() * 360 - 180));