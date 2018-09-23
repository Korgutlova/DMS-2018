SELECT * FROM reservation AS rsrv WHERE rsrv.pk LIKE md5(random_string(40)) || '%'
