# Before running locally:
# export CASSANDRA_HOST="localhost"
import os

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


if __name__ == "__main__":

    auth_provider = PlainTextAuthProvider(username='k8ssandra-superuser', password='ju82V79VmZW9UzUdGZO7')
    cluster = Cluster([os.environ["CASSANDRA_HOST"]],auth_provider = auth_provider)
    session = cluster.connect()

    session.execute('USE mysimbdp;')
    rows = session.execute("SELECT * FROM reviews WHERE marketplace = 'US'")
    for row in rows:
        print(row.product_id,row.marketplace,row.review_body)
