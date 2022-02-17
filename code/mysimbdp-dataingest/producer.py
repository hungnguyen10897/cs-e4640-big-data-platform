import os

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from model import REVIEWS_COLUMNS, REVIEWS_DTYPES

CASSANDRA_HOST = "localhost" if "CASSANDRA_HOST" not in os.environ else os.environ["CASSANDRA_HOST"]

if __name__ == "__main__":

    auth_provider = PlainTextAuthProvider(username='k8ssandra-superuser', password='ju82V79VmZW9UzUdGZO7')
    cluster = Cluster([CASSANDRA_HOST],auth_provider = auth_provider)
    session = cluster.connect()
    session.execute("USE mysimbdp")

    COLUMNS_PLACEHOLDERS = ', '.join(REVIEWS_COLUMNS)
    VALUES_PLACEHOLDERS = ', '.join(len(REVIEWS_COLUMNS) * ["?"])
    INSERT_STMT = f'INSERT INTO reviews ({COLUMNS_PLACEHOLDERS}) VALUES ({VALUES_PLACEHOLDERS});'

    insert_batch = session.prepare(INSERT_STMT)

    with open("./data/amazon_reviews_us_Gift_Card_v1_00.tsv", "r") as f:
        print("Reading file: amazon_reviews_us_Gift_Card_v1_00.tsv")
        i = 0
        f.__next__() # Skip first row
        line = f.readline()
        while line != "":
            print(f"\tInserting line {i}")
            # Get rid of trailing \n
            if line.endswith("\n"):
                line = line[:-1]

            values = line.split("\t")
            
            # Cast to INT
            for index, col in enumerate(REVIEWS_DTYPES.items()):
                if col[1] == "INT":                
                    values[index] = int(values[index])
            
            session.execute(insert_batch, values)
            line = f.readline()
            i+=1

