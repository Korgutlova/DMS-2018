SELECT rs.data FROM reservation as rs WHERE rs.data->>'passenger'=random_string(10);
