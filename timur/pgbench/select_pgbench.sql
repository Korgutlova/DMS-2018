INSERT into reservation (pk, data) VALUES(random_string(30), 
                                          ('{"tickets": [{"place": "' || random_string(3) || 
                                          '", "price":"' || (random() * 80 + 20) ||
                                          '", "flight_no":"' || random_string(4) || 
                                          '", "type": "' || floor(random() * 3) || 
                                          '", "user": {"first_name": "' || random_string(20) ||
                                          '", "last_name":"' || random_string(30) ||
                                          '", "patronymic":"' || random_string(30) ||
                                          '", "email":"' || random_email(20) ||
                                          '"}}], "created_at":"' || clock_timestamp() ||
                                          '", "passenger":"'|| random_email(20) || '"}')::jsonb);