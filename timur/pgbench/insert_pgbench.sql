\set aid random(1000000, 10000000 * :scale)
BEGIN;
SELECT * FROM reservation AS rsrv WHERE rsrv.pk LIKE md5(:aid::text) || '%';
END;
