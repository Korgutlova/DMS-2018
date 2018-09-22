import json
import random
import string
import time
import names
import csv
import psycopg2
import hashlib
from typing import Tuple

RESERVATION_ROW_COUNTS = 1000000


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tickets = list(self.create_tickets(random.randrange(1, 5)))
        self.created_at = int(time.time())
        e = map(lambda x: random.choices((string.ascii_lowercase))[0], range(3))
        self.passenger = "{}@{}.{}".format(*e)
        self.pk = hashlib.md5("{}".format(self.passenger + str(self.created_at)).encode('utf-8')).\
                hexdigest()

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
        self.price = random.uniform(20.0, 100.0)
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
        self.first_name = names.get_first_name()
        self.last_name = names.get_last_name()
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
        for index in range(RESERVATION_ROW_COUNTS):
            r = Reservation()
            writer.writerow({'pk': r.pk, 'data': r.toJson()})
