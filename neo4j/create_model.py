import random
import string

from neo4j import GraphDatabase

t = 3600


class DriverDataBase(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_city(self, filename, N):
        with self._driver.session() as session:
            dictionary = []
            with open(filename, "r", encoding="UTF-8") as file1:
                world_cities = file1.readlines()
                world_cities = world_cities[1:]
                for line in world_cities:
                    arr = line.split(",")
                    dictionary.append(arr[0])
                    # session.write_transaction(self._create_city, arr)
            airplanes = []
            for i in range(int(N / 10)):
                session.write_transaction(self._create_airplane)
            for a in session.write_transaction(self._get_airplanes):
                airplanes.append(a[0])
            for i in range(N):
                flight = session.write_transaction(self._create_flight)
                session.write_transaction(self._create_rel_btw_air_and_flight, flight,
                                          airplanes[random.randint(0, len(airplanes) - 1)])
                city_from = dictionary[random.randint(0, len(dictionary) - 1)]
                city_to = dictionary[random.randint(0, len(dictionary) - 1)]
                if city_to != city_from:
                    session.write_transaction(self._create_rel_btw_cities_and_flight, city_from, city_to, flight)

    @staticmethod
    def _get_airplanes(tx):
        return tx.run("MATCH (a:Airplane) RETURN a.name")

    @staticmethod
    def _create_city(tx, arr):
        tx.run("CREATE (c:City{name: $city, lati: $lati, long: $long})", city=arr[0], lati=float(arr[1]),
               long=float(arr[2]))

    @staticmethod
    def _create_flight(tx):
        flight = get_random_string(5)
        tx.run("CREATE (f:Flight{name: $flight, tense: $tense, duration: $duration, day : $day})",
               flight=flight,
               tense="%s:%s:%s" % (random.randint(0, 23), random.randint(0, 60), random.randint(0, 60)),
               duration=random.randrange(t, t * 12),
               day=random.randint(1, 7))
        return flight

    @staticmethod
    def _create_airplane(tx):
        airplane = get_random_string(5)
        tx.run("CREATE (a:Airplane{name: $name, speed: $speed, type: $type})",
               name=airplane,
               speed=random.randint(1000, 10000),
               type="%s-%s" % (get_random_string(1), get_random_string(3)))
        return airplane

    @staticmethod
    def _create_rel_btw_air_and_flight(tx, flight, airplane):
        tx.run("MATCH (a:Airplane{name: $airplane}), (f:Flight{name: $flight}) CREATE (f)-[:HAS]->(a)",
               airplane=airplane,
               flight=flight)

    @staticmethod
    def _create_rel_btw_cities_and_flight(tx, city_from, city_to, flight):
        tx.run("MATCH (c:City{name:$city_from}), (f:Flight{name:$flight}) CREATE (c)-[:FROM]->(f)",
               city_from=city_from,
               flight=flight)
        tx.run("MATCH (c:City{name:$city_to}), (f:Flight{name:$flight}) CREATE (f)-[:TO]->(c)",
               city_to=city_to,
               flight=flight)


def get_random_string(N: int, case=string.ascii_uppercase) -> str:
    return ''.join(random.choices(case + string.digits, k=N))


if __name__ == "__main__":
    driver = DriverDataBase("bolt://localhost:7687", "neo4j", "password")
    driver.create_city("worldcities.csv", 4000)
    driver.close()
