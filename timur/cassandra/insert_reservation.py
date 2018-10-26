import cassandra
import string
import sys
import time
import os
import random
import threading
import multiprocessing
import argparse
from enum import Enum
from generator import BuildCassandraSQL
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import tuple_factory, SimpleStatement
from cassandra.concurrent import execute_concurrent


QUERY = """
INSERT INTO avia.reservation (passenger, date, tickets ) VALUES ( '{passenger}', toTimestamp(now()), [
    {{
        type: {t},
        place: '{place}',
        price: 213.3,
        flight_number: '{flight_number}',
        passport_data: {{
            email: '{name}',
            first_name: '{name}',
            last_name: '{name}',
            third_name: '{name}'
        }}
    }}
]);
"""

def random_string(k=1):
    return "".join(random.choices(string.ascii_lowercase, k=k))

def generate_random(query:str):
    passenger = random_string(10)
    type_ = random.randint(0, 4)
    place = random_string(3)
    flight_number = random_string(5)
    name = random_string(10)
    return query.format(passenger=passenger,
                        place=place,
                        t=type_,
                        flight_number=flight_number,
                        name=name)

if __name__ == "__main__":
    session = Cluster(("127.0.0.1", ))
    session = session.connect("avia")

    for i in range(1000):
        session.execute(generate_random(QUERY))
