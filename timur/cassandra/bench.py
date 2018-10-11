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
from cassandra.cluster import Cluster
from cassandra.query import tuple_factory

from multiprocessing import Pool, Process, Queue as Q, Lock as L


WORKERS = 2

GLOBAL_SETTINGS = None


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
        SESSIONS = [0] * WORKERS
        if self.connection_class is not None:
            if database == Database.CASSANDRA:
                self.keyspace = kwargs.pop('keyspace', None)
                self.table_name = kwargs.pop('table_name', None)
                self.fields = kwargs.pop('fields', [])
                for session_number in range(WORKERS):
                    SESSIONS[session_number] = self.connection_class(*args, **kwargs)
                    SESSIONS[session_number] = SESSIONS[session_number].connect(self.keyspace)
                    # SESSIONS[session_number].cluster.shutdown()
                    #  SESSIONS[session_number].session.shutdown()
        return SESSIONS

    def run_bench(self, query, session, lock):
        print('RUNNING BENCH. Session: #', session)
        futures = []
        counter = 0
        while True:
            counter += 1
            query = self.generate_query()
            futures.append(session.execute_async(query))

            if counter % 20 == 0:
                for f in futures:
                    row = f.result()
                    print(row)


    def generate_query(self, ):
        if self.database == Database.CASSANDRA:
            query = self.__query.format(keyspace=self.keyspace,
                                               table=self.table_name,
                                               fields=", ".join(self.fields),
                                               values=BuildCassandraSQL.generate_values())
        else:
            raise NotImplementedError("not implement")
        return query

    def create_processes(self, lock):
        for process_no in range(WORKERS):
            p = Process(name=f"{process_no}", target=self.run_bench,
                        args=(self.__query, self.sessions[process_no], lock), daemon=True)
            p.start()


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
                      'args': (['localhost', ],)})
    lock = L()

    processes = bench.create_processes(lock)
    time.sleep(GLOBAL_SETTINGS.time)
    sys.exit()
