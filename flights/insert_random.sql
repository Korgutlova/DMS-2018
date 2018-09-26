create or replace function random_string(length integer)
  returns text as
$$
declare
  chars  text [] := '{A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,0,1,2,3,4,5,6,7,8,9}';
  result text := '';
  i      integer := 0;
begin
  if length < 0
  then
    raise exception 'Given length cannot be less than 0';
  end if;
  for i in 1..length loop
    result := result || chars [1 + random() * (array_length(chars, 1) - 1)];
  end loop;
  return result;
end;
$$
language plpgsql;

do $$
DECLARE
  id_list INT [];
  n       integer;
begin
  select array_agg(id) into id_list from cities order by random() limit 1;
  n := array_length(id_list, 1);
  for r in 1..100000 loop
    INSERT INTO flight (flight_number, from_city_id, to_city_id, airplane_id, day, tense, duration)
    VALUES (random_string((floor(random() * 10) + 1) :: integer),
            floor(random() * n + 1) :: int,
            floor(random() * n + 1) :: int,
            floor(random() * 1000 + 1) :: int,
            floor(random() * 7 + 1) :: int,
            time '00:00' +
            random() * (time '24:00' - time '01:00'),
            floor(random() * 10 + 1) :: int);
  end loop;
end;
$$;