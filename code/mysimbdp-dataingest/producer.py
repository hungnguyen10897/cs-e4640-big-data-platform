import os, configparser
from pathlib import Path

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from model import REVIEWS_COLUMNS, REVIEWS_DTYPES

CASSANDRA_HOST = "localhost" if "CASSANDRA_HOST" not in os.environ else os.environ["CASSANDRA_HOST"]


def insert_data_from_file(file_path):
    with open(file_path, "r") as f:
        i = 0
        f.__next__() # Skip first row
        line = f.readline()
        while line != "":
            if i%10 == 0:
                print(f"\tInserting line {i}")
            # Get rid of trailing \n
            if line.endswith("\n"):
                line = line[:-1]

            values = line.split("\t")
            
            # Cast to INT
            for index, col in enumerate(REVIEWS_DTYPES.items()):
                if col[1] == "INT":                
                    values[index] = int(values[index])
            
            session.execute(insert_statement, values)
            line = f.readline()
            i+=1


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("./credentials.cfg")

    cassandra_username = config.get("CASSANDRA","username")
    cassandra_password = config.get("CASSANDRA","password")

    auth_provider = PlainTextAuthProvider(username=cassandra_username, password=cassandra_password)
    cluster = Cluster([CASSANDRA_HOST],auth_provider = auth_provider)
    session = cluster.connect()
    session.execute("USE mysimbdp")

    COLUMNS_PLACEHOLDERS = ', '.join(REVIEWS_COLUMNS)
    VALUES_PLACEHOLDERS = ', '.join(len(REVIEWS_COLUMNS) * ["?"])
    INSERT_STMT = f'INSERT INTO reviews ({COLUMNS_PLACEHOLDERS}) VALUES ({VALUES_PLACEHOLDERS});'

    insert_statement = session.prepare(INSERT_STMT)

    for path in os.walk("./data"):
        for file_name in path[2]:
            file_path = Path("./data").joinpath(file_name)
            print(f"Writing file: {file_name}")
            insert_data_from_file(file_path)
