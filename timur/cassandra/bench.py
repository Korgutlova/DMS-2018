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

from multiprocessing import Pool, Process, Queue as Q, Lock as L


WORKERS = 2

GLOBAL_SETTINGS = None

COUNTER = 0

def run_bench(p):
    session = Cluster(("127.0.0.1", ))
    session = session.connect("test_keyspace")
    print('RUNNING BENCH. Session: #', session)
    for i in range(1000):
        query = SimpleStatement(Bench.s_generate_query(), consistency_level = ConsistencyLevel.ONE)
        future_res = session.execute(query)


class Database(Enum):
    """Databases section
    """
    CASSANDRA = 0


class Bench:

    SELECT_TYPE = "SELECT"
    INSERT_TYPE = "INSERT"

    __CONNECTION_CLASS = None

    BENCH_DIR =os.path.abspath(os.path.dirname(__file__))


    @property
    def query(self, ):
        return self.__query

    @property
    def connection_class(self, ):
        return self.__CONNECTION_CLASS


    def __init__(self, file_name, database=Database.CASSANDRA, *args, **kwargs):
        self.database = database
        if database == Database.CASSANDRA:
            self.__CONNECTION_CLASS = Cluster
        self.bench_type = type
        self.get_query(file_name)
        self.sessions = self.create_sessions(database, *kwargs.get('args'), **kwargs.get('settings'))

    def get_query(self, file_name):
        query = open(os.path.join(self.BENCH_DIR, file_name), 'r').read()
        self.__query = query

    def create_sessions(self, database, *args, **kwargs):
        pass
        #  SESSIONS = [0] * WORKERS
        #  if self.connection_class is not None:
        #      if database == Database.CASSANDRA:
        #          self.keyspace = kwargs.pop('keyspace', None)
        #          self.table_name = kwargs.pop('table_name', None)
        #          self.fields = kwargs.pop('fields', [])
        #          for session_number in range(WORKERS):
        #              SESSIONS[session_number] = self.connection_class(*args, **kwargs)
        #              SESSIONS[session_number] = SESSIONS[session_number].connect(self.keyspace)
        #              query = self.generate_query()
        #              SESSIONS[session_number].execute(query)
        #  return SESSIONS


    @classmethod
    def generate_query(cls, ):
        query = "INSERT INTO {keyspace}.{table} ({fields}) VALUES ({values});".format(keyspace="test_keyspace",
                                           table="users",
                                           fields=", ".join(['name', 'email']),
                                           values=BuildCassandraSQL.generate_values())
        return query

    @classmethod
    def s_generate_query(cls, ):
        char = "".join(random.choices(string.ascii_lowercase, k=10))
        query = "SELECT * FROM {keyspace}.{table} WHERE {condition};".format(keyspace="test_keyspace",
                                           table="users",
                                           condition=f"email='{char}'")
        return query

    def create_processes(self, lock):
        p = Pool(WORKERS)
        p.map(run_bench, range(WORKERS))
        p.close()
        p.join()
        print('mapped')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Benchmark database')
    parser.add_argument('--file-name', '-f', required=True, nargs='?', help='file path of bench file')
    parser.add_argument('--time', nargs='?', required=True, type=int, help='time of bench')
    parser.add_argument('--pc', nargs='?', type=int, default=4, help='the count of processes')

    GLOBAL_SETTINGS = parser.parse_args()
    WORKERS = GLOBAL_SETTINGS.pc

    bench = Bench(database=Database.CASSANDRA, file_name=GLOBAL_SETTINGS.file_name,
                  **{'settings': {
                      'keyspace': 'test_keyspace',
                      'table_name': 'users',
                      'fields': ['email', 'name'],
                      'port': 9042,},
                      'args': (['127.0.0.1',],)})
    lock = L()

    r = time.time()
    processes = bench.create_processes(lock)
    e = time.time()
    print(f"Pools: {WORKERS}")
    print(f'Executed 10000 queries each of workers')
    print(WORKERS * 1000 / (e-r))
