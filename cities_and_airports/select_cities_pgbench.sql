select * from cities where name = random_string((floor(random() * 30) + 4)::integer)
