create or replace function random_email(length integer) returns text as
$$
declare
  chars text[] := '{mail.ru, gmail.com, aol.com, mail.com}';
  result text := '';
  i integer := 0;
begin
  result := random_string(length) || '@' || chars[1+random()*(array_length(chars, 1)-1)]
  return result;
end;
$$ language plpgsql;