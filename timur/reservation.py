import json
import random
import string
import time
import names
import csv
import psycopg2
import hashlib
from typing import Tuple
from multiprocessing import Pool, Process, Queue

RESERVATION_ROW_COUNTS = 500


class JsonSerializable(object):

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def toJson(self, ):
        data = self.__dict__
        data.pop('pk')
        return json.dumps(data)

    def get_random_string(self, N: int, case=string.ascii_uppercase) -> str:
        return ''.join(random.choices(case + string.digits, k=N))


class Reservation(JsonSerializable):
    passenger: str  # email by default PK
    created_at: str
    tickets: Tuple[list, tuple] = []

    __domains: tuple = ("hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com")

    def return_md5(self, q, string: str):
        return q.put(hashlib.md5(string.encode('utf-8')).hexdigest())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tickets = list(self.create_tickets(random.randrange(1, 5)))
        self.created_at = time.time()
        self.passenger = "{}@{}".format(self.get_random_string(N=10), random.choices(self.__domains)[0])
        q1 = Queue(); q2 = Queue()
        p1 = Process(target=self.return_md5, args=(q1, self.passenger))
        p2 = Process(target=self.return_md5, args=(q2, str(self.created_at)))
        p1.start(); p2.start();
        p1.join(); p2.join();
        self.pk = q1.get() + q2.get()

    def create_tickets(self, length=1) -> object:
        for i in range(length):
            yield Ticket().__dict__


class Ticket(JsonSerializable):
    FLIGHT_COUNTS = 1000000

    TYPES = {
        0: "Low",
        1: "Medium",
        2: "High",
    }

    place: str
    price: float = 0.0
    flight_no: str
    type: int = list(TYPES.keys())[0]
    user: object

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.place = self.get_random_string(3)
        self.price = round(random.uniform(20.0, 100.0), 1)
        self.flight_no = self.get_random_string(4)
        self.type = random.choices(list(self.TYPES.keys()))[0]
        self.user = self.create_user().__dict__

    def create_user(self, ):
        return User()


class User(JsonSerializable):
    passport: str
    first_name: str
    last_name: str
    patronymic: str
    email: str

    __domains: tuple = ("hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_name = self.get_random_string(10)
        self.last_name = self.get_random_string(10)
        self.patronymic = ""
        self.email = "{}@{}".format(self.get_random_string(10, case=string.ascii_lowercase),
                                    random.choices(self.domains)[0])

    @property
    def domains(self, ):
        return self.__domains


if __name__ == "__main__":
    with open('out_data/reservation.csv', 'w') as csv_file:
        fieldnames = ['pk', 'data']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        processes = []
        for index in range(RESERVATION_ROW_COUNTS):
            r = Reservation()
            writer.writerow({'pk': r.pk, 'data': r.toJson()})
