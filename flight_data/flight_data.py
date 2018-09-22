import argparse
import json
import random
import string
import sys
import time
from hashlib import md5

import psycopg2


class DbConnection:
    def __init__(self, connection_params: dict):
        self.connection_params = connection_params
        self.conn = None

    def get_conn(self):
        if not self.conn is None:
            return self.conn
        self.conn = psycopg2.connect(**self.connection_params)
        self.conn.autocommit = True
        return self.conn


def random_flight_data() -> dict:
    return {
        'pk': md5(str(time.time()).join(
            random.choices(string.ascii_uppercase, k=2) + random.choices(string.digits, k=5)).encode(
            'utf-8')).hexdigest(),
        'speed': random.randrange(1, 1000),
        'height': random.randrange(1, 10000),
        'remaining_distance': random.randrange(500, 100000),
        'temperature_overboard': random.randrange(-100, -30),
        'engine_condition': random.choices(['good', 'normal', 'bad', 'trouble'])[0],
        'weather_condition': random.choices(['sunny', 'cloudy', 'rainy', 'foggy'])[0]
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('database', help='db name')
    parser.add_argument('user', help='db user')
    parser.add_argument('password', help='db user password')
    parser.add_argument('--host', help='db host')
    parser.add_argument('--insert-count', help='insert count')
    args = parser.parse_args()

    connection_parameters = {
        'host': args.host or 'localhost',
        'dbname': args.database,
        'user': args.user,
        'password': args.password
    }
    conn = DbConnection(connection_parameters).get_conn()
    count = int(args.insert_count)
    #
    # try:
    #     with conn.cursor() as cursor:
    #         cursor.execute(
    #             """CREATE TABLE if not exists flight_data (id serial primary key,data jsonb);""")
    #         while count > 0:
    #             cursor.execute("""INSERT INTO flight_data (data) VALUES ('{}');""".format(
    #                 json.dumps(random_flight_data())
    #             ))
    #             count -= 1
    #     sys.stdout.write('Created database environment successfully.\n')
    # except psycopg2.Error:
    #     raise SystemExit(
    #         'Failed to setup Postgres environment.\n{0}'.format(sys.exc_info())
    #     )
    # finally:
    #     conn.close()
