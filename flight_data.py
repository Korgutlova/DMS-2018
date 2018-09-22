import argparse
import base64
import json
import random
import sys
import time

import psycopg2
import pyDes


class EncodeDecodeUtil:
    # нам же пофиг на секретность, да?
    __key = 'verysecretkey___'
    __iv = '00000000'

    @classmethod
    def encode(cls, data: str):
        encrypted = pyDes.triple_des(
            cls.__key, pyDes.CBC, cls.__iv,
            pad=None, padmode=pyDes.PAD_PKCS5
        ).encrypt(data)
        return base64.b64encode(encrypted).decode('utf-8')

    @classmethod
    def decode(cls, data: str):
        decrypted = pyDes.triple_des(
            cls.__key, pyDes.CBC, cls.__iv,
            pad=None, padmode=pyDes.PAD_PKCS5
        ).decrypt(base64.b64decode(data))
        return decrypted.decode('utf-8')


class DbConnection:
    def __init__(self, connection_params: dict):
        self.connection_params = connection_params
        self.conn = None

    def get_conn(self):
        if not self.conn is None:
            return self.conn
        self.conn = psycopg2.connect(**connection_parameters)
        self.conn.autocommit = True
        return self.conn


def random_flight_data() -> dict:
    return {
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
    parser.add_argument('--insert-count', help='db host')
    args = parser.parse_args()

    connection_parameters = {
        'host': args.host or 'localhost',
        'database': args.database,
        'user': args.user,
        'password': args.password
    }
    conn = DbConnection(connection_parameters).get_conn()
    count = int(args.insert_count)

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE if not exists flight_data (flight_number_and_date varchar(255) primary key,data jsonb);""")
            while count > 0:
                flight_number_and_date = '{}.{}'.format(EncodeDecodeUtil.encode(f'{random.randrange(1,100000000000)}'),
                                                        EncodeDecodeUtil.encode(f'{time.time()}'))
                cursor.execute("""INSERT INTO flight_data (flight_number_and_date,data) VALUES ('{}','{}');""".format(
                    flight_number_and_date, json.dumps(random_flight_data())
                ))
                count -= 1
        sys.stdout.write('Created database environment successfully.\n')
    except psycopg2.Error:
        raise SystemExit(
            'Failed to setup Postgres environment.\n{0}'.format(sys.exc_info())
        )
    finally:
        conn.close()
