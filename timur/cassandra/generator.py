import cassandra
import string
import os
import random
from multiprocessing import Pool, Process, Queue as Q

WORKERS = 4

class User:
    email: str
    name: str

class BuildCassandraSQL:
    DIRNAME = 'data'
    FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), DIRNAME))
    FILES: dict = {
        'INSERT': 'insert__{}',
        'SELECT': 'select__{}',
    }
    QUERY: dict = {
        "INSERT": "INSERT INTO {keyspace}.{table} ({fields}) VALUES ({values});\n",
        "SELECT": "SELECT * FROM {keyspace}.{table} WHERE {condition};\n",
    }
    DOMAINS: tuple = (
            'gmail.com', 'yandex.ru', 'mail.ru', 'tatnet.ru', 'test4.com')

    def __init__(self, *args, **kwargs):
        self.workers = kwargs.pop('workers', 1)
        self.count_inserts = kwargs.pop('count_inserts', 50)
        self.count_select = kwargs.pop('count_select', 50)
        self.keyspace = kwargs.pop('keyspace', 'default')
        self.table_name = kwargs.pop('table_name', 'default')
        self.fields = kwargs.pop('fields', [])
        super().__init__(*args, **kwargs)

    @classmethod
    def generate_values(cls, ):
        domain = random.choice(cls.DOMAINS)
        random_email = "".join(random.choices(string.ascii_lowercase, k=20)) + domain
        random_name = "".join(random.choices(string.ascii_lowercase, k=10)).title()
        return f"'{random_email}', '{random_name}'"

    def generate_condition(self, param="email"):
        return param + "=" + "".join(random.choices(string.ascii_lowercase, k=10))

    def build_queries(self, ):
        insert_query = self.QUERY['INSERT']
        values = self.generate_values()
        insert_query = insert_query.format(keyspace=self.keyspace,
                                           table=self.table_name,
                                           fields=", ".join(self.fields),
                                           values=values)
                    #  select_query = self.QUERY['SELECT']
                    #  values = self.generate_condition()
                    #  select_query = select_query.format(keyspace=self.keyspace,
                    #                                     table=self.table_name,
                    #                                     condition=values)
                    #  filewriter.write(select_query)



if __name__ == "__main__":
    bcs = BuildCassandraSQL(workers=WORKERS,
                            count_inserts=1000000,
                            count_select=1000000,
                            keyspace="test_keyspace",
                            table_name="users",
                            fields=['email', 'name'])
    bcs.build_queries()

